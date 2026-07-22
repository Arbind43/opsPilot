"""
OpsPilot — Pinecone Client
=============================
Manages connections to the Pinecone vector database.
"""

import os
import logging
from app.config import get_settings

logger = logging.getLogger(__name__)

class PineconeClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PineconeClient, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
            
        settings = get_settings()
        self.api_key = settings.PINECONE_API_KEY
        self.index_name = settings.PINECONE_INDEX_NAME
        self.pc = None
        self.index = None
        
        try:
            from pinecone import Pinecone
            
            if not self.api_key:
                logger.warning("PINECONE_API_KEY is not set. Operating in stub mode.")
                self._initialized = True
                return
                
            self.pc = Pinecone(api_key=self.api_key)
            self.index = self.pc.Index(self.index_name)
            self._initialized = True
            logger.info("Pinecone client initialized successfully.")
        except ImportError:
            logger.warning("pinecone-client python package not installed. Operating in stub mode.")
            self._initialized = True
        except Exception as e:
            logger.error(f"Failed to connect to Pinecone: {e}")
            self._initialized = True

    def heartbeat(self):
        if not self.index:
            raise Exception("Pinecone client is not connected.")
        return self.index.describe_index_stats()

    def get_index(self):
        if not self.index:
            logger.warning("Pinecone Stub: get_index called.")
            return None
        return self.index

# Global singleton instance
pinecone_client = PineconeClient()
