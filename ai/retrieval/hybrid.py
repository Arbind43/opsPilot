"""
OpsPilot — Hybrid Search Coordinator
=======================================
Combines Vector Search (ChromaDB) and Graph Search (Neo4j), returning a unified, ranked context.
"""

import logging
import asyncio
from typing import List, Dict, Any

from ai.retrieval.vector_search import VectorSearch
from ai.retrieval.graph_search import GraphSearch
from ai.retrieval.reranker import Reranker

logger = logging.getLogger(__name__)

class HybridRetriever:
    def __init__(self):
        self.vector_search = VectorSearch()
        self.graph_search = GraphSearch()
        self.reranker = Reranker()

    async def retrieve_context(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Executes parallel searches across both vector and graph DBs, combines, and reranks.
        """
        logger.info(f"Executing hybrid search for: '{query}'")
        
        # Execute both searches concurrently
        vector_results, graph_results = await asyncio.gather(
            self.vector_search.search(query, top_k=top_k),
            self.graph_search.search(query, top_k=top_k)
        )
        
        # Combine
        combined_results = vector_results + graph_results
        
        # Rerank
        final_results = await self.reranker.rerank(query, combined_results, top_k=top_k)
        
        logger.info(f"Hybrid search returned {len(final_results)} ranked context items.")
        return final_results
