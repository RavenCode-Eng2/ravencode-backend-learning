from typing import List, Optional, Dict, Any
from ...DB.database import LESSONS_COLLECTION
from ...models.lessons.lesson import Lesson, LessonCreate, LessonUpdate
from ..base import BaseService
from ...core.decorators import cached

class LessonService(BaseService):
    def __init__(self):
        super().__init__(LESSONS_COLLECTION)
    
    @cached("lesson", invalidate_patterns=["lesson:*", "module_lessons:*"])
    async def create_lesson(self, lesson: LessonCreate) -> Lesson:
        """Create a new lesson."""
        # Ensure the order is unique within the module
        if await self.exists({"module_id": lesson.module_id, "order": lesson.order}):
            # If order exists, shift all lessons with >= order up by 1
            collection = await self.get_collection()
            await collection.update_many(
                {
                    "module_id": lesson.module_id,
                    "order": {"$gte": lesson.order}
                },
                {"$inc": {"order": 1}}
            )
        
        lesson_dict = await self.create(lesson)
        return Lesson.model_validate(lesson_dict)
    
    @cached("lesson")
    async def get_lesson(self, lesson_id: str) -> Optional[Lesson]:
        """Get a lesson by ID."""
        lesson_dict = await self.get_by_id(lesson_id)
        return Lesson.model_validate(lesson_dict) if lesson_dict else None
    
    @cached("module_lessons")
    async def list_lessons(
        self,
        module_id: str,
        skip: int = 0,
        limit: int = 100,
        include_archived: bool = False
    ) -> List[Lesson]:
        """List lessons for a module."""
        filter_query: Dict[str, Any] = {"module_id": module_id}
        
        if not include_archived:
            filter_query["status"] = {"$ne": "archived"}
            
        lessons = await self.get_all(
            skip=skip,
            limit=limit,
            filter_query=filter_query,
            sort=[("order", 1)]  # Sort by order ascending
        )
        return [Lesson.model_validate(lesson) for lesson in lessons]
    
    @cached("lesson", invalidate_patterns=["lesson:*", "module_lessons:*"])
    async def update_lesson(self, lesson_id: str, lesson_update: LessonUpdate) -> Optional[Lesson]:
        """Update a lesson."""
        current_lesson = await self.get_lesson(lesson_id)
        if not current_lesson:
            return None
            
        # If order is being updated, handle reordering
        if lesson_update.order is not None and lesson_update.order != current_lesson.order:
            collection = await self.get_collection()
            if lesson_update.order > current_lesson.order:
                # Moving down: decrease order of lessons in between
                await collection.update_many(
                    {
                        "module_id": current_lesson.module_id,
                        "order": {"$gt": current_lesson.order, "$lte": lesson_update.order}
                    },
                    {"$inc": {"order": -1}}
                )
            else:
                # Moving up: increase order of lessons in between
                await collection.update_many(
                    {
                        "module_id": current_lesson.module_id,
                        "order": {"$gte": lesson_update.order, "$lt": current_lesson.order}
                    },
                    {"$inc": {"order": 1}}
                )
        
        lesson_dict = await self.update(lesson_id, lesson_update)
        return Lesson.model_validate(lesson_dict) if lesson_dict else None
    
    @cached("lesson", invalidate_patterns=["lesson:*", "module_lessons:*"])
    async def delete_lesson(self, lesson_id: str) -> bool:
        """Delete a lesson."""
        current_lesson = await self.get_lesson(lesson_id)
        if not current_lesson:
            return False
            
        # Shift all lessons with higher order down by 1
        collection = await self.get_collection()
        await collection.update_many(
            {
                "module_id": current_lesson.module_id,
                "order": {"$gt": current_lesson.order}
            },
            {"$inc": {"order": -1}}
        )
        
        return await self.delete(lesson_id)
    
    async def update_lesson_sequence(
        self,
        lesson_id: str,
        next_lesson_id: Optional[str] = None,
        previous_lesson_id: Optional[str] = None
    ) -> Optional[Lesson]:
        """Update the next/previous lesson sequence."""
        update_data: Dict[str, Any] = {}
        
        if next_lesson_id is not None:
            update_data["next_lesson_id"] = next_lesson_id
        if previous_lesson_id is not None:
            update_data["previous_lesson_id"] = previous_lesson_id
            
        if not update_data:
            return await self.get_lesson(lesson_id)
            
        collection = await self.get_collection()
        result = await collection.update_one(
            {"_id": lesson_id},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            return None
            
        return await self.get_lesson(lesson_id)
    
    async def update_lesson_metrics(
        self,
        lesson_id: str,
        total_views: Optional[int] = None,
        average_time_spent: Optional[int] = None,
        completion_count: Optional[int] = None
    ) -> Optional[Lesson]:
        """Update lesson metrics."""
        update_data: Dict[str, Any] = {}
        
        if total_views is not None:
            update_data["total_views"] = total_views
        if average_time_spent is not None:
            update_data["average_time_spent"] = average_time_spent
        if completion_count is not None:
            update_data["completion_count"] = completion_count
            
        if not update_data:
            return await self.get_lesson(lesson_id)
            
        collection = await self.get_collection()
        result = await collection.update_one(
            {"_id": lesson_id},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            return None
            
        return await self.get_lesson(lesson_id) 