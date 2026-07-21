"""
OpsPilot — Vector Search
===========================
Executes semantic similarity search against the ChromaDB vector database.
"""

import logging
from typing import List, Dict, Any
from ai.llm_factory import get_embedding_model

logger = logging.getLogger(__name__)

class VectorSearch:
    def __init__(self, collection_name: str = "opspilot_docs"):
        self.collection_name = collection_name
        
        try:
            from app.db.chroma_client import chroma_client
            self.client = chroma_client
            self.collection = self.client.get_or_create_collection(self.collection_name)
        except ImportError:
            logger.warning("chroma_client not available. Operating in stub mode.")
            self.client = None
            self.collection = None

    async def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Queries ChromaDB for chunks semantically similar to the user query.
        """
        if not self.collection:
            logger.warning(f"VectorSearch Stub: Would have searched for '{query}'")
            return []
            
        try:
            # Generate the embedding for the query explicitly using Gemini
            embedder = get_embedding_model()
            query_embedding = await embedder.aembed_query(query)
            
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )
            
            # Reformat ChromaDB output to a standard list of dictionaries
            formatted_results = []
            
            # ChromaDB query returns dict of lists: { 'documents': [[...]], 'metadatas': [[...]], 'distances': [[...]] }
            if results and results.get("documents") and len(results["documents"]) > 0:
                docs = results["documents"][0]
                metas = results["metadatas"][0] if results.get("metadatas") else [{}] * len(docs)
                dists = results["distances"][0] if results.get("distances") else [0.0] * len(docs)
                
                for doc, meta, dist in zip(docs, metas, dists):
                    formatted_results.append({
                        "type": "vector_chunk",
                        "content": doc,
                        "metadata": meta,
                        "score": dist
                    })
                    
            return formatted_results
            
        except Exception as e:
            logger.error(f"Vector search failed: {e}")
            return []
