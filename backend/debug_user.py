
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

async def check_user():
    load_dotenv()
    mongodb_url = os.getenv("MONGODB_URL")
    database_name = os.getenv("DATABASE_NAME")
    
    client = AsyncIOMotorClient(mongodb_url)
    db = client[database_name]
    
    user = await db.users.find_one({"email": "alemanisha952@gmail.com"})
    if user:
        print(f"✅ Found user: {user.get('full_name')} ({user.get('email')})")
        print(f"Full Record: {user}")
    else:
        print("❌ User not found")
    client.close()

if __name__ == "__main__":
    asyncio.run(check_user())
