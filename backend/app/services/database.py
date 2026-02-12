from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
import logging
import certifi

class Database:
    client: AsyncIOMotorClient = None
    db = None

db = Database()

async def connect_to_mongo():
    try:
        db.client = AsyncIOMotorClient(
            settings.MONGODB_URL,
            serverSelectionTimeoutMS=5000, # 5 second timeout
            tlsCAFile=certifi.where()
        )
        db.db = db.client[settings.DATABASE_NAME]
        # Verify connection
        await db.client.admin.command('ping')
        logging.info("Successfully connected to MongoDB")
    except Exception as e:
        logging.error(f"Could not connect to MongoDB: {e}")
        # We don't raise here to allow the app to start, 
        # but operations will fail with clear timeout errors
        pass

async def close_mongo_connection():
    db.client.close()
    logging.info("Closed MongoDB connection")

async def get_database():
    return db.db
