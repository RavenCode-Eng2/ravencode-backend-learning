from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

# MongoDB connection settings
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb+srv://dchicuasuque:7jdNLSir1SHD75hm@cluster0.mongodb.net/?retryWrites=true&w=majority&appName=RavenCodeLearning")
DATABASE_NAME = os.getenv("DATABASE_NAME", "RavenCodeLearning")

# Collection names
COURSES_COLLECTION = "courses"
MODULES_COLLECTION = "modules"
LESSONS_COLLECTION = "lessons"
ASSESSMENTS_COLLECTION = "assessments"
PROGRESS_COLLECTION = "progress"
ROADMAPS_COLLECTION = "roadmaps"

# Database instance
_db: Optional[AsyncIOMotorDatabase] = None

async def get_database() -> AsyncIOMotorDatabase:
    """
    Get the database instance. Creates a new connection if one doesn't exist.
    
    Returns:
        AsyncIOMotorDatabase: The database instance
    """
    global _db
    if _db is None:
        client = AsyncIOMotorClient(MONGODB_URL)
        _db = client[DATABASE_NAME]
        
        # Create indexes for our collections
        await _create_indexes()
    
    return _db

async def _create_indexes():
    """
    Creates indexes for all collections in the database.
    This ensures optimal query performance.
    """
    db = await get_database()
    
    # Courses indexes
    await db[COURSES_COLLECTION].create_index("instructor_id")
    await db[COURSES_COLLECTION].create_index([("title", "text"), ("description", "text")])
    await db[COURSES_COLLECTION].create_index("status")
    
    # Modules indexes
    await db[MODULES_COLLECTION].create_index("course_id")
    await db[MODULES_COLLECTION].create_index([("order", 1), ("course_id", 1)], unique=True)
    
    # Lessons indexes
    await db[LESSONS_COLLECTION].create_index("module_id")
    await db[LESSONS_COLLECTION].create_index("course_id")
    await db[LESSONS_COLLECTION].create_index([("order", 1), ("module_id", 1)], unique=True)
    
    # Assessments indexes
    await db[ASSESSMENTS_COLLECTION].create_index("module_id")
    await db[ASSESSMENTS_COLLECTION].create_index("course_id")
    
    # Progress indexes
    await db[PROGRESS_COLLECTION].create_index([("user_id", 1), ("course_id", 1)], unique=True)
    await db[PROGRESS_COLLECTION].create_index("user_id")
    await db[PROGRESS_COLLECTION].create_index("course_id")

async def test_connection() -> bool:
    """
    Tests the MongoDB connection and returns True if successful, False otherwise.
    
    Returns:
        bool: True if the connection is successful, False otherwise.
    """
    try:
        db = await get_database()
        await db.command('ping')
        print("✅ MongoDB connection successful!")
        return True
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return False

async def close_database():
    """
    Closes the MongoDB database connection.
    """
    global _db
    if _db is not None:
        _db.client.close()
        _db = None
        print("MongoDB connection closed.")
