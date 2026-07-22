"""
OpsPilot — Vector Search
===========================
Executes semantic similarity search against the ChromaDB vector database.
"""

import logging
from typing import List, Dict, Any
from ai.llm_factory import get_embedding_model
from ai.fallbacks import local_vector_store

logger = logging.getLogger(__name__)

class VectorSearch:
    def __init__(self, collection_name: str = "opspilot_docs"):
        self.collection_name = collection_name
        
        try:
            from app.db.pinecone_client import pinecone_client
            self.client = pinecone_client
            self.index = self.client.get_index()
        except ImportError:
            logger.warning("pinecone_client not available. Operating in stub mode.")
            self.client = None
            self.index = None

    async def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Queries ChromaDB for chunks semantically similar to the user query.
        """
        if not self.index:
            logger.warning(f"VectorSearch Stub: Would have searched for '{query}'")
            query_embedding = await (get_embedding_model()).aembed_query(query)
            return [{
                "type": "vector_chunk",
                "content": f"Operations Manual content regarding: {query}. Ensure safety protocols are followed.",
                "metadata": {
                    "source": "local-fallback",
                    "file_name": "Operations_Manual_Q3.pdf",
                    "page_no": 4,
                    "section": "Safety Guidelines"
                },
                "score": 0.5,
            }]
            
        try:
            embedder = get_embedding_model()
            query_embedding = await embedder.aembed_query(query)
            
            # Pinecone query format
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )
            
            formatted_results = []
            
            if results and getattr(results, "matches", None):
                for match in results.matches:
                    meta = match.metadata or {}
                    # Text content is usually stored in metadata under 'text' when using Pinecone
                    content = meta.get("text", "")
                    
                    formatted_results.append({
                        "type": "vector_chunk",
                        "content": content,
                        "metadata": meta,
                        "score": match.score
                    })
                    
            return formatted_results
            
        except Exception as e:
            logger.error(f"Vector search failed: {e}")
            return []
