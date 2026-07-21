"""
OpsPilot — ChromaDB Client
=============================
Manages connections to the local ChromaDB instance for vector storage.
"""

import os
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class ChromaClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChromaClient, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
            
        self.host = os.getenv("CHROMA_HOST", "localhost")
        self.port = int(os.getenv("CHROMA_PORT", "8000"))
        self.client = None
        
        try:
            import chromadb
            # Connecting to the ChromaDB HTTP server running in docker
            self.client = chromadb.HttpClient(host=self.host, port=self.port)
            self._initialized = True
            logger.info("ChromaDB client initialized successfully.")
        except ImportError:
            logger.warning("chromadb python package not installed. Operating in stub mode.")
            self._initialized = True
        except Exception as e:
            logger.error(f"Failed to connect to ChromaDB: {e}")
            self._initialized = True

    def heartbeat(self):
        if not self.client:
            raise Exception("Chroma client is not connected.")
        return self.client.heartbeat()

    def get_or_create_collection(self, name: str):
        if not self.client:
            logger.warning("Chroma Stub: get_or_create_collection called.")
            return None
        
        try:
            return self.client.get_or_create_collection(name=name)
        except Exception as e:
            logger.error(f"Failed to get/create ChromaDB collection '{name}': {e}")
            return None

# Global singleton instance
chroma_client = ChromaClient()
