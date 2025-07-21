from typing import Any, Dict, List, Optional, Type, TypeVar, cast
from bson import ObjectId
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorCollection

from ..DB.database import get_database

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseService:
    def __init__(self, collection_name: str):
        self.collection_name = collection_name
    
    async def get_collection(self) -> AsyncIOMotorCollection:
        db = await get_database()
        return db[self.collection_name]
    
    async def create(self, create_schema: CreateSchemaType) -> ModelType:
        """Create a new document in the collection."""
        collection = await self.get_collection()
        data = create_schema.model_dump(exclude_unset=True)
        result = await collection.insert_one(data)
        created_doc = await self.get_by_id(str(result.inserted_id))
        if not created_doc:
            raise ValueError("Failed to create document")
        return cast(ModelType, created_doc)
    
    async def get_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        """Get a document by its ID."""
        collection = await self.get_collection()
        if not ObjectId.is_valid(id):
            return None
        result = await collection.find_one({"_id": ObjectId(id)})
        return result if result else None
    
    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        filter_query: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Get all documents with pagination and filtering."""
        collection = await self.get_collection()
        cursor = collection.find(filter_query or {}).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)
    
    async def update(
        self,
        id: str,
        update_schema: UpdateSchemaType
    ) -> Optional[Dict[str, Any]]:
        """Update a document by its ID."""
        collection = await self.get_collection()
        if not ObjectId.is_valid(id):
            return None
            
        update_data = update_schema.model_dump(exclude_unset=True)
        if not update_data:
            return await self.get_by_id(id)
            
        result = await collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            return None
            
        return await self.get_by_id(id)
    
    async def delete(self, id: str) -> bool:
        """Delete a document by its ID."""
        collection = await self.get_collection()
        if not ObjectId.is_valid(id):
            return False
            
        result = await collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0
    
    async def count(self, filter_query: Optional[Dict[str, Any]] = None) -> int:
        """Count documents in the collection with optional filtering."""
        collection = await self.get_collection()
        return await collection.count_documents(filter_query or {})
    
    async def exists(self, filter_query: Dict[str, Any]) -> bool:
        """Check if a document exists with the given filter."""
        collection = await self.get_collection()
        count = await collection.count_documents(filter_query, limit=1)
        return count > 0 