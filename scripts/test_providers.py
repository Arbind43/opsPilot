"""
OpsPilot — Provider Diagnostic Script
=======================================
Tests LLM (Groq), Embedding (Gemini), and Pinecone connectivity.
Run from the opspilot/ root:
    python scripts/test_providers.py
"""

import sys
import os
import asyncio
import time

# Add backend to path so app imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Load .env
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))


def print_section(title: str):
    print(f"\n{'='*55}")
    print(f"  {title}")
    print('='*55)

def ok(msg): print(f"  ✅  {msg}")
def fail(msg): print(f"  ❌  {msg}")
def warn(msg): print(f"  ⚠️   {msg}")
def info(msg): print(f"  ℹ️   {msg}")


# ─── 1. ENV VARS ───────────────────────────────────────
print_section("1. Environment Variables")

required = {
    "GROQ_API_KEY":            os.getenv("GROQ_API_KEY", ""),
    "GROQ_MODEL":              os.getenv("GROQ_MODEL", ""),
    "GOOGLE_API_KEY":          os.getenv("GOOGLE_API_KEY", ""),
    "GEMINI_EMBEDDING_MODEL":  os.getenv("GEMINI_EMBEDDING_MODEL", ""),
    "PINECONE_API_KEY":        os.getenv("PINECONE_API_KEY", ""),
    "PINECONE_INDEX_NAME":     os.getenv("PINECONE_INDEX_NAME", ""),
    "MONGO_URI":               os.getenv("MONGO_URI", ""),
    "REDIS_URL":               os.getenv("REDIS_URL", ""),
    "LLM_PROVIDER":            os.getenv("LLM_PROVIDER", ""),
    "EMBEDDING_PROVIDER":      os.getenv("EMBEDDING_PROVIDER", ""),
}

for key, val in required.items():
    if val:
        masked = val[:8] + "..." + val[-4:] if len(val) > 12 else "***"
        ok(f"{key} = {masked}")
    else:
        fail(f"{key} is NOT SET")


# ─── 2. GROQ LLM ───────────────────────────────────────
print_section("2. Groq LLM — Quick Inference Test")
try:
    from langchain_groq import ChatGroq
    groq_key = os.getenv("GROQ_API_KEY")
    groq_model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    if not groq_key:
        fail("GROQ_API_KEY missing — skipping test")
    else:
        info(f"Model: {groq_model}")
        t0 = time.time()
        llm = ChatGroq(model_name=groq_model, groq_api_key=groq_key, temperature=0.0)
        response = llm.invoke("Reply with exactly: OK")
        elapsed = time.time() - t0
        content = str(response.content).strip()
        ok(f"Response: '{content}' ({elapsed:.2f}s)")
except ImportError:
    fail("langchain-groq not installed. Run: pip install langchain-groq")
except Exception as e:
    fail(f"Groq LLM error: {e}")


# ─── 3. GEMINI EMBEDDING ───────────────────────────────
print_section("3. Gemini Embedding — Embed Test")
try:
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    google_key = os.getenv("GOOGLE_API_KEY")
    embed_model = os.getenv("GEMINI_EMBEDDING_MODEL", "models/text-embedding-004")

    if not google_key:
        fail("GOOGLE_API_KEY missing — skipping test")
    else:
        info(f"Model: {embed_model}")
        t0 = time.time()
        embedder = GoogleGenerativeAIEmbeddings(
            model=embed_model,
            google_api_key=google_key,
        )
        vectors = embedder.embed_documents(["OpsPilot test embedding"])
        elapsed = time.time() - t0
        dim = len(vectors[0]) if vectors else 0
        ok(f"Embedding dimensions: {dim}  ({elapsed:.2f}s)")
        if dim == 0:
            fail("Returned empty embedding vector!")
except ImportError:
    fail("langchain-google-genai not installed. Run: pip install langchain-google-genai")
except Exception as e:
    fail(f"Gemini Embedding error: {e}")


# ─── 4. PINECONE ───────────────────────────────────────
print_section("4. Pinecone — Index Connectivity Test")
try:
    from pinecone import Pinecone
    pc_key = os.getenv("PINECONE_API_KEY")
    pc_index = os.getenv("PINECONE_INDEX_NAME", "opspilot")

    if not pc_key:
        fail("PINECONE_API_KEY missing — skipping test")
    else:
        info(f"Index: {pc_index}")
        t0 = time.time()
        pc = Pinecone(api_key=pc_key)
        index_list = [i.name for i in pc.list_indexes()]
        elapsed = time.time() - t0
        ok(f"Available indexes: {index_list}  ({elapsed:.2f}s)")
        if pc_index in index_list:
            idx = pc.Index(pc_index)
            stats = idx.describe_index_stats()
            ok(f"Index '{pc_index}' stats: total_vector_count={stats.get('total_vector_count', 0)}")
            # Check dimension matches Gemini embedding (768)
            dim = stats.get('dimension', None)
            if dim:
                info(f"Index dimension: {dim}")
                if dim != 768:
                    warn(f"Index dimension {dim} may not match Gemini embedding (768)!")
        else:
            warn(f"Index '{pc_index}' not found in account. Available: {index_list}")
            warn("You may need to create the index first.")
except ImportError:
    fail("pinecone not installed. Run: pip install pinecone")
except Exception as e:
    fail(f"Pinecone error: {e}")


# ─── 5. MONGODB ────────────────────────────────────────
print_section("5. MongoDB — Connection Test")
async def test_mongo():
    try:
        from motor.motor_asyncio import AsyncIOMotorClient
        mongo_uri = os.getenv("MONGO_URI")
        mongo_db = os.getenv("MONGO_DB", "opspilot")
        if not mongo_uri:
            fail("MONGO_URI missing — skipping test")
            return
        t0 = time.time()
        client = AsyncIOMotorClient(mongo_uri, serverSelectionTimeoutMS=8000)
        await client.admin.command("ping")
        elapsed = time.time() - t0
        db = client[mongo_db]
        collections = await db.list_collection_names()
        ok(f"Connected to MongoDB ({elapsed:.2f}s)")
        ok(f"Database '{mongo_db}' collections: {collections}")
        
        # Count stuck documents
        docs_col = db["documents"]
        total = await docs_col.count_documents({})
        pending = await docs_col.count_documents({"processing_status": "pending"})
        processing = await docs_col.count_documents({"processing_status": "processing"})
        completed = await docs_col.count_documents({"processing_status": "completed"})
        failed = await docs_col.count_documents({"processing_status": "failed"})
        info(f"Documents — total:{total}  pending:{pending}  processing:{processing}  completed:{completed}  failed:{failed}")
        client.close()
    except Exception as e:
        fail(f"MongoDB error: {e}")

asyncio.run(test_mongo())


# ─── 6. REDIS / CELERY ─────────────────────────────────
print_section("6. Redis — Broker Connectivity Test")
try:
    import redis
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    masked_url = redis_url[:30] + "..." if len(redis_url) > 30 else redis_url
    info(f"URL: {masked_url}")
    t0 = time.time()
    r = redis.from_url(redis_url, socket_connect_timeout=8, ssl_cert_reqs=None)
    pong = r.ping()
    elapsed = time.time() - t0
    if pong:
        ok(f"Redis PONG received ({elapsed:.2f}s)")
    else:
        fail("Redis did not respond to PING")
except ImportError:
    fail("redis not installed. Run: pip install redis")
except Exception as e:
    fail(f"Redis error: {e}")


# ─── SUMMARY ───────────────────────────────────────────
print_section("Diagnostic Complete")
print("  If any ❌ appear above, fix those before running the worker.\n")
