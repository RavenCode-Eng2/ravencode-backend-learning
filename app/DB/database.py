from typing import Optional
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

# MongoDB connection settings
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb+srv://dchicuasuque:7jdNLSir1SHD75hm@cluster0.mongodb.net/?retryWrites=true&w=majority&appName=RavenCodeLearning")
DATABASE_NAME = os.getenv("DATABASE_NAME", "RavenCodeLearning")

def get_database(db_name: str = DATABASE_NAME) -> Optional[MongoClient]:
    """
    Obtains the MongoDB database connection using MongoDB Atlas connection string.
    
    Args:
        db_name (str): The database name to connect to (default is "RavenCodeLearning").
    
    Returns:
        MongoClient: The MongoDB client connected to the specified database.
        None: If the connection fails.
    """
    try:
        # Get MongoDB URL from environment variable or use the default
        client = MongoClient(MONGODB_URL)
        db = client[db_name]
        return db
    except Exception as e:
        print(f"Error al conectar con MongoDB: {e}")
        return None

def test_connection():
    """
    Tests the MongoDB connection and returns True if successful, False otherwise.
    Prints a message indicating the result of the connection attempt.
    
    Returns:
        bool: True if the connection is successful, False otherwise.
    """
    try:
        # Test the connection using the MongoDB URL
        client = MongoClient(MONGODB_URL)
        # Test the connection by pinging the server
        client.admin.command('ping')
        print("✅ MongoDB connection successful!")
        return True
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return False
    finally:
        if 'client' in locals():
            client.close()

def close_database(client: MongoClient):
    """
    Closes the MongoDB database connection.
    
    Args:
        client (MongoClient): The MongoClient instance to close.
        
    Prints a message when the connection is closed.
    """
    if client:
        client.close()
        print("MongoDB connection closed.")
