"""
OpsPilot — Neo4j Database Client
==================================
Manages connections and transactions with the Neo4j graph database.
"""

import os
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class Neo4jClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Neo4jClient, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
            
        self.uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = os.getenv("NEO4J_USER", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD", "password")
        self.driver = None
        
        try:
            from neo4j import AsyncGraphDatabase
            self.driver = AsyncGraphDatabase.driver(self.uri, auth=(self.user, self.password))
            self._initialized = True
            logger.info("Neo4j driver initialized successfully.")
        except ImportError:
            logger.warning("neo4j python package not installed. Operating in stub mode.")
            self._initialized = True
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            self._initialized = True

    def verify_connectivity(self):
        if not self.driver:
            raise Exception("Neo4j driver is not connected.")
        # Synchronous verify connectivity for app startup
        import asyncio
        loop = asyncio.get_event_loop()
        if loop.is_running():
            return self.driver.verify_connectivity()
        else:
            return loop.run_until_complete(self.driver.verify_connectivity())

    async def close(self):
        if self.driver:
            await self.driver.close()
            logger.info("Neo4j connection closed.")

    async def execute_query(self, query: str, parameters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Execute a Cypher query asynchronously.
        """
        if not self.driver:
            logger.warning(f"Neo4j Stub: Executing query (driver not connected):\n{query}\nParams: {parameters}")
            return []

        if parameters is None:
            parameters = {}
            
        async with self.driver.session() as session:
            try:
                result = await session.run(query, parameters)
                records = await result.data()
                return records
            except Exception as e:
                logger.error(f"Cypher query execution failed: {e}")
                raise

# Global singleton instance
neo4j_client = Neo4jClient()
