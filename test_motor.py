from motor.motor_asyncio import AsyncIOMotorClient
client = AsyncIOMotorClient()
db = client['test']
print('db.client:', getattr(db, 'client', None))
