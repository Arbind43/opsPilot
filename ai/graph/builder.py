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
            # We execute node creation sequentially to avoid deadlocks
            for entity in entities:
                label = entity.get("label", "Entity")
                node_id = entity.get("id")
                props = entity.get("properties", {})
                
                # Cypher injection safety: labels must be alphanumeric
                clean_label = "".join(c for c in label if c.isalnum()) or "Entity"
                
                query = f"""
                MERGE (n:{clean_label} {{id: $id}})
                SET n += $props, n.last_updated = timestamp()
                RETURN n
                """
                
                # In Neo4j we generally pass parameters for security and caching
                await self.client.execute_query(query, parameters={"id": node_id, "props": props})

            # Execute relation creation
            for rel in relations:
                source = rel.get("source")
                target = rel.get("target")
                rel_type = rel.get("type", "RELATED_TO")
                props = rel.get("properties", {})
                
                # Cypher injection safety
                clean_type = "".join(c for c in rel_type.upper() if c.isalnum() or c == '_') or "RELATED_TO"
                
                query = f"""
                MATCH (s {{id: $source_id}})
                MATCH (t {{id: $target_id}})
                MERGE (s)-[r:{clean_type}]->(t)
                SET r += $props, r.last_updated = timestamp()
                """
                
                await self.client.execute_query(query, parameters={
                    "source_id": source,
                    "target_id": target,
                    "props": props
                })
                
            logger.info("Graph update complete.")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update graph: {e}")
            return False
