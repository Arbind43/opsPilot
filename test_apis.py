import asyncio
import os
import sys
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Add backend directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

async def test_mongo():
    print("\n--- Testing MongoDB & Beanie ---")
    from motor.motor_asyncio import AsyncIOMotorClient
    # Patch for compatibility between Beanie and newer Motor versions
    AsyncIOMotorClient.append_metadata = lambda self, *args, **kwargs: None
    from beanie import init_beanie
    from app.models.document import Document

    uri = os.getenv("MONGO_URI")
    db_name = os.getenv("MONGO_DB")
    print(f"Connecting to MongoDB: {db_name}")
    try:
        client = AsyncIOMotorClient(uri)
        db = client[db_name]
        await init_beanie(database=db, document_models=[Document])
        print("[SUCCESS] MongoDB & Beanie initialized successfully!")
        
        # Count documents
        doc_count = await Document.count()
        print(f"Total documents in database: {doc_count}")
        client.close()
    except Exception as e:
        print(f"[FAILURE] MongoDB Error: {e}")

async def test_pinecone():
    print("\n--- Testing Pinecone ---")
    api_key = os.getenv("PINECONE_API_KEY")
    index_name = os.getenv("PINECONE_INDEX_NAME")
    print(f"Index name: {index_name}")
    try:
        from pinecone import Pinecone
        pc = Pinecone(api_key=api_key)
        index = pc.Index(index_name)
        stats = index.describe_index_stats()
        print("[SUCCESS] Pinecone connected successfully!")
        print(f"Index stats: {stats}")
    except Exception as e:
        print(f"[FAILURE] Pinecone Error: {e}")

async def test_neo4j():
    print("\n--- Testing Neo4j ---")
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USER")
    password = os.getenv("NEO4J_PASSWORD")
    try:
        from neo4j import AsyncGraphDatabase
        driver = AsyncGraphDatabase.driver(uri, auth=(user, password))
        await driver.verify_connectivity()
        print("[SUCCESS] Neo4j connected and verified successfully!")
        await driver.close()
    except Exception as e:
        print(f"[FAILURE] Neo4j Error: {e}")

async def test_gemini_embeddings():
    print("\n--- Testing Gemini Embeddings ---")
    google_key = os.getenv("GOOGLE_API_KEY")
    model_name = os.getenv("GEMINI_EMBEDDING_MODEL", "models/gemini-embedding-2")
    try:
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        embeddings = GoogleGenerativeAIEmbeddings(model=model_name, google_api_key=google_key)
        vector = await embeddings.aembed_query("Hello world, testing RAG embeddings.")
        print(f"[SUCCESS] Gemini Embeddings generated successfully! Dimension: {len(vector)}")
    except Exception as e:
        print(f"[FAILURE] Gemini Embeddings Error: {e}")

async def test_groq_llm():
    print("\n--- Testing Groq LLM ---")
    groq_key = os.getenv("GROQ_API_KEY")
    model_name = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    try:
        from langchain_groq import ChatGroq
        llm = ChatGroq(model_name=model_name, groq_api_key=groq_key)
        response = await llm.ainvoke("Write a short sentence saying hello.")
        print(f"[SUCCESS] Groq LLM responded successfully!")
        print(f"Response: {response.content}")
    except Exception as e:
        print(f"[FAILURE] Groq LLM Error: {e}")

async def main():
    await test_mongo()
    await test_pinecone()
    await test_neo4j()
    await test_gemini_embeddings()
    await test_groq_llm()

if __name__ == "__main__":
    asyncio.run(main())
