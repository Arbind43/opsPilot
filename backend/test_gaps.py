import asyncio, sys, os
sys.path.append(os.getcwd())
sys.path.append(os.path.dirname(os.getcwd()))
from app.api.v1.documents import get_knowledge_gaps
from app.db.session import init_db
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.getcwd()), '.env'))

async def main():
    await init_db()
    print(await get_knowledge_gaps('test_user'))

if __name__ == '__main__':
    asyncio.run(main())
