"""
OpsPilot — Graph Search
==========================
Executes Cypher queries against Neo4j to retrieve structured entity relationships.
"""

import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class GraphSearch:
    def __init__(self):
        try:
            from app.db.neo4j_client import neo4j_client
            self.client = neo4j_client
        except ImportError:
            logger.warning("neo4j_client not available. Operating in stub mode.")
            self.client = None

    async def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Uses an LLM (or heuristics) to extract entities from the query, 
        then queries Neo4j for their subgraph.
        """
        if not self.client:
            logger.warning(f"GraphSearch Stub: Would have searched graph for '{query}'")
            return []

        # 1. Entity Extraction from Query
        # In a real environment, you'd use a lightweight LLM or Named Entity Recognition
        # to pull out specific asset names or locations from the query.
        extracted_entities = self._extract_entities_from_query(query)
        
        if not extracted_entities:
            # Fallback: full-text search on Neo4j nodes if configured, 
            # or just return nothing if no explicit entities matched.
            return []

        results = []
        try:
            # 2. Cypher Query
            # This query matches the extracted entity and returns it along with 
            # its immediate neighbors to provide surrounding context.
            cypher = """
            MATCH (n)
            WHERE n.id IN $entity_ids OR toLower(n.name) IN $entity_ids
            OPTIONAL MATCH (n)-[r]-(m)
            RETURN n, r, m
            LIMIT $limit
            """
            
            records = await self.client.execute_query(
                cypher, 
                parameters={"entity_ids": extracted_entities, "limit": top_k * 5}
            )
            
            # 3. Format results into human-readable / LLM-readable context strings
            for record in records:
                source = record.get("n", {})
                relation = record.get("r", {})
                target = record.get("m", {})
                
                if relation and target:
                    # Example: "(Pump) [LOCATED_IN] (Boiler Room)"
                    context_str = f"({source.get('id', 'Unknown')}) [{relation[1]}] ({target.get('id', 'Unknown')})"
                else:
                    # Just the isolated node
                    context_str = f"Entity: {source.get('id', 'Unknown')} (Type: {source.get('label', 'Unknown')})"
                    
                results.append({
                    "type": "graph_relation",
                    "content": context_str,
                    "metadata": {"source": "Neo4j"},
                    "score": 1.0  # Graph relations are exact matches
                })
                
        except Exception as e:
            logger.error(f"Graph search failed: {e}")
            
        return results

    def _extract_entities_from_query(self, query: str) -> List[str]:
        """
        Heuristic / Stub extraction.
        """
        query_lower = query.lower()
        entities = []
        # Hardcoded for demonstration. An LLM agent would do this dynamically.
        if "pump" in query_lower:
            entities.append("pump")
        if "compressor" in query_lower:
            entities.append("compressor")
        if "boiler" in query_lower:
            entities.append("boiler")
        return entities
