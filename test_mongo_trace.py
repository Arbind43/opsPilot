import asyncio, os, traceback
from dotenv import load_dotenv
load_dotenv()
async def main():
    from motor.motor_asyncio import AsyncIOMotorClient
    # Monkey-patch AsyncIOMotorClient to support append_metadata for Beanie compatibility
    AsyncIOMotorClient.append_metadata = lambda self, *args, **kwargs: None
    
    from beanie import init_beanie
    from app.models.user import User
    try:
        client = AsyncIOMotorClient(os.getenv('MONGO_URI'))
        db = client[os.getenv('MONGO_DB')]
        await init_beanie(database=db, document_models=[User])
        print("Successfully initialized beanie!")
    except Exception as e:
        traceback.print_exc()
if __name__ == '__main__':
    asyncio.run(main())
