"""
OpsPilot — Vector Embedder
=============================
Generates vector embeddings for text chunks and stores them in ChromaDB.
"""

import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class VectorEmbedder:
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

    async def embed_and_store(self, chunks: List[Dict[str, Any]], document_id: str) -> bool:
        """
        Takes a list of chunk dictionaries, generates embeddings, and saves to ChromaDB.
        """
        if not chunks:
            return True

        if not self.collection:
            logger.warning("VectorEmbedder Stub: Would have embedded and stored chunks.")
            return False
            
        logger.info(f"Generating embeddings for {len(chunks)} chunks.")

        ids = []
        documents = []
        metadatas = []

        for chunk in chunks:
            # We prefix the chunk ID with the document ID for global uniqueness
            chunk_id = f"{document_id}_{chunk['id']}"
            ids.append(chunk_id)
            documents.append(chunk["text"])
            
            # Merge document_id into metadata
            meta = chunk.get("metadata", {})
            meta["document_id"] = document_id
            metadatas.append(meta)

        try:
            # 1. Generate embeddings using our configured LLM factory
            from ai.llm_factory import get_embedding_model
            embedder = get_embedding_model()
            
            # Extract texts for embedding
            texts_to_embed = [doc for doc in documents]
            embeddings = await embedder.aembed_documents(texts_to_embed)

            # 2. Add to ChromaDB with explicit embeddings
            self.collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas,
                embeddings=embeddings
            )
            logger.info("Successfully stored embeddings in ChromaDB.")
            return True
        except Exception as e:
            logger.error(f"Failed to store embeddings: {e}")
            return False
