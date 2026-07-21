"""
OpsPilot — Entity & Relation Extractor
========================================
Uses Google Gemini via LangChain to extract structured Knowledge Graph
nodes and edges from industrial document text.
"""

import json
import logging
from typing import Dict, Any, List

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from ai.llm_factory import get_llm

logger = logging.getLogger(__name__)

EXTRACTION_PROMPT = """You are an industrial knowledge graph extraction engine.

Extract all entities and relationships from the following industrial document text.

Return ONLY valid JSON — no markdown, no explanation, just the JSON object.

JSON format:
{{
  "entities": [
    {{"id": "unique_id", "label": "EntityType", "properties": {{"name": "...", "key": "value"}}}}
  ],
  "relations": [
    {{"source": "source_id", "target": "target_id", "type": "RELATION_TYPE", "properties": {{}}}}
  ]
}}

Entity types to extract:
- Asset (equipment, machines, instruments, valves, pumps, compressors, tanks, pipes)
- Component (parts, sub-components, bearings, seals, motors)
- Location (plant areas, zones, buildings, floors)
- Person (engineers, technicians, operators — use role if name unknown)
- Procedure (SOPs, maintenance tasks, inspection steps)
- Regulation (ISO standards, OSHA requirements, Factory Act clauses)
- Parameter (temperature, pressure, flow rate, RPM, voltage — include units)
- Failure (failure modes, defects, faults, malfunctions)
- MaintenanceEvent (work orders, inspections, overhauls)
- Document (manuals, reports, certificates — reference by title)

Relation types to use:
- LOCATED_IN, PART_OF, CONNECTED_TO, MAINTAINED_BY, INSPECTED_BY
- CAUSED_BY, LEADS_TO, REQUIRES, REGULATED_BY
- HAS_PARAMETER, HAS_COMPONENT, DOCUMENTED_IN
- PERFORMED_ON, REFERENCES, APPLIES_TO

Text to process:
{text}

Return ONLY the JSON object:"""


class KnowledgeExtractor:
    def __init__(self):
        self._chain = None

    def _get_chain(self):
        if self._chain is None:
            llm = get_llm(temperature=0.0)
            prompt = ChatPromptTemplate.from_template(EXTRACTION_PROMPT)
            self._chain = prompt | llm | StrOutputParser()
        return self._chain

    def extract(self, parsed_doc: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synchronous wrapper — calls async extract internally.
        For use in Celery tasks.
        """
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    future = pool.submit(asyncio.run, self._extract_async(parsed_doc))
                    return future.result()
            else:
                return loop.run_until_complete(self._extract_async(parsed_doc))
        except Exception as e:
            logger.error(f"Extraction failed, falling back to heuristics: {e}")
            return self._heuristic_full_doc(parsed_doc)

    async def _extract_async(self, parsed_doc: Dict[str, Any]) -> Dict[str, Any]:
        """Async version of extract."""
        all_entities = []
        all_relations = []

        doc_title = parsed_doc.get("title", "Unknown Document")
        all_entities.append({
            "id": doc_title,
            "label": "Document",
            "properties": {"name": doc_title}
        })

        sections = parsed_doc.get("sections", [])
        chain = self._get_chain()

        for section in sections:
            header = section.get("header", "Section")
            content = section.get("content", "")
            if not content or len(content) < 50:
                continue

            # Truncate very long sections to fit token limits
            text_chunk = content[:3000]

            try:
                raw = await chain.ainvoke({"text": text_chunk})
                # Clean the response — sometimes model wraps in ```json
                raw = raw.strip()
                if raw.startswith("```"):
                    raw = raw.split("```")[1]
                    if raw.startswith("json"):
                        raw = raw[4:]
                data = json.loads(raw)
                all_entities.extend(data.get("entities", []))
                all_relations.extend(data.get("relations", []))
            except (json.JSONDecodeError, Exception) as e:
                logger.warning(f"LLM extraction failed for section '{header}': {e}. Using heuristics.")
                fallback = self._heuristic_extraction(content)
                all_entities.extend(fallback.get("entities", []))
                all_relations.extend(fallback.get("relations", []))

            # Always add the section node and link it to the document
            all_entities.append({
                "id": f"{doc_title}::{header}",
                "label": "Section",
                "properties": {"name": header, "document": doc_title}
            })
            all_relations.append({
                "source": doc_title,
                "target": f"{doc_title}::{header}",
                "type": "HAS_SECTION",
                "properties": {}
            })

        return {
            "entities": self._deduplicate_entities(all_entities),
            "relations": self._deduplicate_relations(all_relations),
        }

    def _heuristic_extraction(self, text: str) -> Dict[str, List[Dict[str, Any]]]:
        """Fallback keyword-based extraction when LLM is unavailable."""
        entities = []
        relations = []
        lower = text.lower()

        keywords = {
            "pump": "Asset", "compressor": "Asset", "valve": "Asset",
            "motor": "Asset", "boiler": "Asset", "turbine": "Asset",
            "bearing": "Component", "seal": "Component", "impeller": "Component",
            "temperature": "Parameter", "pressure": "Parameter", "flow": "Parameter",
        }
        for kw, label in keywords.items():
            if kw in lower:
                entities.append({"id": kw.capitalize(), "label": label, "properties": {"name": kw.capitalize()}})

        return {"entities": entities, "relations": relations}

    def _heuristic_full_doc(self, parsed_doc: Dict[str, Any]) -> Dict[str, Any]:
        entities = []
        relations = []
        for section in parsed_doc.get("sections", []):
            result = self._heuristic_extraction(section.get("content", ""))
            entities.extend(result["entities"])
            relations.extend(result["relations"])
        return {
            "entities": self._deduplicate_entities(entities),
            "relations": self._deduplicate_relations(relations),
        }

    def _deduplicate_entities(self, entities: List[Dict]) -> List[Dict]:
        seen, deduped = set(), []
        for e in entities:
            if e["id"] not in seen:
                seen.add(e["id"])
                deduped.append(e)
        return deduped

    def _deduplicate_relations(self, relations: List[Dict]) -> List[Dict]:
        seen, deduped = set(), []
        for r in relations:
            sig = f"{r['source']}-{r['type']}-{r['target']}"
            if sig not in seen:
                seen.add(sig)
                deduped.append(r)
        return deduped
