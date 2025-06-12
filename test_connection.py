# test_connection.py
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# MongoDB connection URL from .env
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb+srv://dchicuasuque:7jdNLSir1SHD75hm@ravencodelearning.msujdft.mongodb.net/?retryWrites=true&w=majority&appName=RavenCodeLearning")


def test_connection():
    """
    Tests the MongoDB connection and prints a success message if the connection is successful.
    """
    try:
        # Try to connect to MongoDB using the provided connection string
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

# Run the test
test_connection()
