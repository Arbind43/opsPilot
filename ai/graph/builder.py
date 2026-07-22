"""
OpsPilot — Graph Builder
===========================
Constructs and executes Cypher queries to build the Knowledge Graph in Neo4j.
"""

import logging
import asyncio
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class GraphBuilder:
    def __init__(self):
        try:
            from app.db.neo4j_client import neo4j_client
            self.client = neo4j_client
        except ImportError:
            logger.warning("Could not import neo4j_client. Graph operations will fail.")
            self.client = None

    async def update_graph(self, graph_data: Dict[str, Any], document_id: str = None) -> bool:
        """
        Takes standardized graph_data (entities, relations) and merges them into Neo4j.
        """
        if not self.client:
            return False

        entities = graph_data.get("entities", [])
        relations = graph_data.get("relations", [])

        if not entities and not relations:
            return True

        logger.info(f"Updating graph with {len(entities)} nodes and {len(relations)} edges.")

        try:
            from collections import defaultdict
            
            # Batch node creation grouped by label
            entities_by_label = defaultdict(list)
            for entity in entities:
                label = entity.get("label", "Entity")
                clean_label = "".join(c for c in label if c.isalnum()) or "Entity"
                entities_by_label[clean_label].append({
                    "id": entity.get("id"),
                    "props": entity.get("properties", {})
                })

            for label, batch in entities_by_label.items():
                query = f"""
                UNWIND $batch AS row
                MERGE (n:{label} {{id: row.id}})
                SET n += row.props, n.last_updated = timestamp()
                """
                await self.client.execute_query(query, parameters={"batch": batch})

            # Batch relation creation grouped by type
            relations_by_type = defaultdict(list)
            for rel in relations:
                rel_type = rel.get("type", "RELATED_TO")
                clean_type = "".join(c for c in rel_type.upper() if c.isalnum() or c == '_') or "RELATED_TO"
                relations_by_type[clean_type].append({
                    "source_id": rel.get("source"),
                    "target_id": rel.get("target"),
                    "props": rel.get("properties", {})
                })

            for rel_type, batch in relations_by_type.items():
                query = f"""
                UNWIND $batch AS row
                MATCH (s {{id: row.source_id}})
                MATCH (t {{id: row.target_id}})
                MERGE (s)-[r:{rel_type}]->(t)
                SET r += row.props, r.last_updated = timestamp()
                """
                await self.client.execute_query(query, parameters={"batch": batch})
                
            logger.info("Graph update complete.")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update graph: {e}")
            return False
