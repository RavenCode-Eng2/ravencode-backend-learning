from typing import List, Optional, Dict, Any
from ...DB.database import MODULES_COLLECTION
from ...models.modules.module import Module, ModuleCreate, ModuleUpdate
from ..base import BaseService

class ModuleService(BaseService):
    def __init__(self):
        super().__init__(MODULES_COLLECTION)
    
    async def create_module(self, module: ModuleCreate) -> Module:
        """Create a new module."""
        # Ensure the order is unique within the course
        if await self.exists({"course_id": module.course_id, "order": module.order}):
            # If order exists, shift all modules with >= order up by 1
            collection = await self.get_collection()
            await collection.update_many(
                {
                    "course_id": module.course_id,
                    "order": {"$gte": module.order}
                },
                {"$inc": {"order": 1}}
            )
        
        module_dict = await self.create(module)
        return Module.model_validate(module_dict)
    
    async def get_module(self, module_id: str) -> Optional[Module]:
        """Get a module by ID."""
        module_dict = await self.get_by_id(module_id)
        return Module.model_validate(module_dict) if module_dict else None
    
    async def list_modules(
        self,
        course_id: str,
        skip: int = 0,
        limit: int = 100,
        include_archived: bool = False
    ) -> List[Module]:
        """List modules for a course."""
        filter_query: Dict[str, Any] = {"course_id": course_id}
        
        if not include_archived:
            filter_query["status"] = {"$ne": "archived"}
            
        modules = await self.get_all(
            skip=skip,
            limit=limit,
            filter_query=filter_query
        )
        return [Module.model_validate(module) for module in modules]
    
    async def update_module(self, module_id: str, module_update: ModuleUpdate) -> Optional[Module]:
        """Update a module."""
        current_module = await self.get_module(module_id)
        if not current_module:
            return None
            
        # If order is being updated, handle reordering
        if module_update.order is not None and module_update.order != current_module.order:
            collection = await self.get_collection()
            if module_update.order > current_module.order:
                # Moving down: decrease order of modules in between
                await collection.update_many(
                    {
                        "course_id": current_module.course_id,
                        "order": {"$gt": current_module.order, "$lte": module_update.order}
                    },
                    {"$inc": {"order": -1}}
                )
            else:
                # Moving up: increase order of modules in between
                await collection.update_many(
                    {
                        "course_id": current_module.course_id,
                        "order": {"$gte": module_update.order, "$lt": current_module.order}
                    },
                    {"$inc": {"order": 1}}
                )
        
        module_dict = await self.update(module_id, module_update)
        return Module.model_validate(module_dict) if module_dict else None
    
    async def delete_module(self, module_id: str) -> bool:
        """Delete a module."""
        current_module = await self.get_module(module_id)
        if not current_module:
            return False
            
        # Shift all modules with higher order down by 1
        collection = await self.get_collection()
        await collection.update_many(
            {
                "course_id": current_module.course_id,
                "order": {"$gt": current_module.order}
            },
            {"$inc": {"order": -1}}
        )
        
        return await self.delete(module_id)
    
    async def add_lesson_to_module(self, module_id: str, lesson_id: str) -> Optional[Module]:
        """Add a lesson to a module's lesson list."""
        collection = await self.get_collection()
        result = await collection.update_one(
            {"_id": module_id},
            {"$addToSet": {"lesson_ids": lesson_id}}
        )
        if result.modified_count == 0:
            return None
        return await self.get_module(module_id)
    
    async def add_assessment_to_module(self, module_id: str, assessment_id: str) -> Optional[Module]:
        """Add an assessment to a module's assessment list."""
        collection = await self.get_collection()
        result = await collection.update_one(
            {"_id": module_id},
            {"$addToSet": {"assessment_ids": assessment_id}}
        )
        if result.modified_count == 0:
            return None
        return await self.get_module(module_id)
    
    async def remove_lesson_from_module(self, module_id: str, lesson_id: str) -> Optional[Module]:
        """Remove a lesson from a module's lesson list."""
        collection = await self.get_collection()
        result = await collection.update_one(
            {"_id": module_id},
            {"$pull": {"lesson_ids": lesson_id}}
        )
        if result.modified_count == 0:
            return None
        return await self.get_module(module_id)
    
    async def remove_assessment_from_module(self, module_id: str, assessment_id: str) -> Optional[Module]:
        """Remove an assessment from a module's assessment list."""
        collection = await self.get_collection()
        result = await collection.update_one(
            {"_id": module_id},
            {"$pull": {"assessment_ids": assessment_id}}
        )
        if result.modified_count == 0:
            return None
        return await self.get_module(module_id)
    
    async def update_module_completion(
        self,
        module_id: str,
        completion_percentage: float,
        total_students_enrolled: Optional[int] = None,
        average_completion_time: Optional[int] = None
    ) -> Optional[Module]:
        """Update module completion metrics."""
        update_data: Dict[str, Any] = {
            "completion_percentage": completion_percentage
        }
        
        if total_students_enrolled is not None:
            update_data["total_students_enrolled"] = total_students_enrolled
        if average_completion_time is not None:
            update_data["average_completion_time"] = average_completion_time
            
        collection = await self.get_collection()
        result = await collection.update_one(
            {"_id": module_id},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            return None
            
        return await self.get_module(module_id) 