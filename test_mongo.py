import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def test_mongo():
    from motor.motor_asyncio import AsyncIOMotorClient
    from beanie import init_beanie
    from app.models.user import User

    uri = os.getenv("MONGO_URI")
    db_name = os.getenv("MONGO_DB")
    
    print(f"Connecting to {db_name}")
    client = AsyncIOMotorClient(uri)
    db = client[db_name]
    
    try:
        await init_beanie(database=db, document_models=[User])
        print("Beanie init successful!")
    except Exception as e:
        print(f"Error: {type(e).__name__} - {e}")

if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))
    asyncio.run(test_mongo())
