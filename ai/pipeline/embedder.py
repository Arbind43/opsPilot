"""
OpsPilot — Vector Embedder
=============================
Generates vector embeddings for text chunks and stores them in ChromaDB.
"""

import logging
from typing import List, Dict, Any

from ai.fallbacks import local_vector_store

logger = logging.getLogger(__name__)

class VectorEmbedder:
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

    async def embed_and_store(self, chunks: List[Dict[str, Any]], document_id: str) -> bool:
        """
        Takes a list of chunk dictionaries, generates embeddings, and saves to ChromaDB.
        """
        if not chunks:
            return True

        if not self.index:
            logger.warning("VectorEmbedder Stub: Would have embedded and stored chunks.")
            local_vector_store.upsert(vectors=[{"id": f"{document_id}_fallback", "metadata": {"text": "demo fallback"}, "values": [0.0] * 32}])
            return False
            
        logger.info(f"Generating embeddings for {len(chunks)} chunks.")

        vectors = []
        documents = []

        for chunk in chunks:
            chunk_id = f"{document_id}_{chunk['id']}"
            documents.append(chunk["text"])
            
            meta = chunk.get("metadata", {})
            meta["document_id"] = document_id
            # Pinecone requires storing the text inside metadata since it doesn't have a separate documents field
            meta["text"] = chunk["text"]
            
            # Store temporarily without embedding, we'll add the embedding in the next step
            vectors.append({
                "id": chunk_id,
                "metadata": meta
            })

        try:
            from ai.llm_factory import get_embedding_model
            embedder = get_embedding_model()
            
            embeddings = await embedder.aembed_documents(documents)

            # Zip the generated embeddings into the vector dictionaries
            for i, vec in enumerate(vectors):
                vec["values"] = embeddings[i]

            # Upsert into Pinecone
            self.index.upsert(vectors=vectors)
            logger.info("Successfully stored embeddings in Pinecone.")
            return True
        except Exception as e:
            logger.error(f"Failed to store embeddings: {e}")
            return False
