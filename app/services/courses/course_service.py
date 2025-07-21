from typing import List, Optional, Dict, Any
from ...DB.database import COURSES_COLLECTION, MODULES_COLLECTION, LESSONS_COLLECTION
from ...models.courses.course import Course, CourseCreate, CourseUpdate
from ..base import BaseService

class CourseService(BaseService):
    def __init__(self):
        super().__init__(COURSES_COLLECTION)
    
    async def create_course(self, course: CourseCreate) -> Course:
        """Create a new course."""
        course_dict = await self.create(course)
        return Course.model_validate(course_dict)
    
    async def get_course(self, course_id: str) -> Optional[Course]:
        """Get a course by ID."""
        course_dict = await self.get_by_id(course_id)
        return Course.model_validate(course_dict) if course_dict else None
    
    async def list_courses(
        self,
        skip: int = 0,
        limit: int = 10,
        instructor_id: Optional[str] = None,
        category: Optional[str] = None,
        level: Optional[str] = None,
        language: Optional[str] = None,
        status: Optional[str] = None,
        search_term: Optional[str] = None
    ) -> List[Course]:
        """List courses with filtering and search."""
        filter_query: Dict[str, Any] = {}
        
        if instructor_id:
            filter_query["instructor_id"] = instructor_id
        if category:
            filter_query["category"] = category
        if level:
            filter_query["level"] = level
        if language:
            filter_query["language"] = language
        if status:
            filter_query["status"] = status
        if search_term:
            filter_query["$text"] = {"$search": search_term}
        
        courses = await self.get_all(skip=skip, limit=limit, filter_query=filter_query)
        return [Course.model_validate(course) for course in courses]
    
    async def update_course(self, course_id: str, course_update: CourseUpdate) -> Optional[Course]:
        """Update a course."""
        course_dict = await self.update(course_id, course_update)
        return Course.model_validate(course_dict) if course_dict else None
    
    async def delete_course(self, course_id: str) -> bool:
        """Delete a course."""
        return await self.delete(course_id)
    
    async def add_module_to_course(self, course_id: str, module_id: str) -> Optional[Course]:
        """Add a module to a course's module list."""
        collection = await self.get_collection()
        result = await collection.update_one(
            {"_id": course_id},
            {"$addToSet": {"module_ids": module_id}}
        )
        if result.modified_count == 0:
            return None
        return await self.get_course(course_id)
    
    async def remove_module_from_course(self, course_id: str, module_id: str) -> Optional[Course]:
        """Remove a module from a course's module list."""
        collection = await self.get_collection()
        result = await collection.update_one(
            {"_id": course_id},
            {"$pull": {"module_ids": module_id}}
        )
        if result.modified_count == 0:
            return None
        return await self.get_course(course_id)
    
    async def update_course_metrics(
        self,
        course_id: str,
        total_students: Optional[int] = None,
        average_rating: Optional[float] = None,
        total_ratings: Optional[int] = None,
        completion_rate: Optional[float] = None
    ) -> Optional[Course]:
        """Update course metrics."""
        update_data: Dict[str, Any] = {}
        
        if total_students is not None:
            update_data["metrics.total_students"] = total_students
        if average_rating is not None:
            update_data["metrics.average_rating"] = average_rating
        if total_ratings is not None:
            update_data["metrics.total_ratings"] = total_ratings
        if completion_rate is not None:
            update_data["metrics.completion_rate"] = completion_rate
            
        if not update_data:
            return await self.get_course(course_id)
            
        collection = await self.get_collection()
        result = await collection.update_one(
            {"_id": course_id},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            return None
            
        return await self.get_course(course_id)
    
    async def get_courses_with_modules_and_lessons(self) -> List[Dict[str, Any]]:
        """Get all courses with their modules and lessons structured for frontend."""
        # Get all courses
        courses = await self.list_courses(limit=100, status="published")
        
        result = []
        
        for course in courses:
            # Get modules for this course
            modules_collection = await self.get_db_collection(MODULES_COLLECTION)
            modules_cursor = modules_collection.find(
                {"course_id": str(course.id)},
                sort=[("order", 1)]
            )
            modules = await modules_cursor.to_list(length=None)
            
            course_modules = []
            for module in modules:
                # Get lessons for this module
                lessons_collection = await self.get_db_collection(LESSONS_COLLECTION)
                lessons_cursor = lessons_collection.find(
                    {"module_id": str(module["_id"])},
                    sort=[("order", 1)]
                )
                lessons = await lessons_cursor.to_list(length=None)
                
                # Format lessons for frontend
                module_lessons = []
                for lesson in lessons:
                    module_lessons.append({
                        "title": lesson.get("title", ""),
                        "description": lesson.get("description", ""),
                        "route": lesson.get("route", f"/lesson/{lesson['_id']}")
                    })
                
                # Format module for frontend
                course_modules.append({
                    "id": str(module["_id"]),
                    "title": module.get("title", ""),
                    "description": module.get("description", ""),
                    "lessons": module_lessons
                })
            
            # Format course for frontend
            result.append({
                "id": str(course.id),
                "title": course.title,
                "description": course.description,
                "image": getattr(course, 'image_url', f"https://via.placeholder.com/400x200?text={course.title}"),
                "modules": course_modules
            })
        
        return result
    
    async def get_db_collection(self, collection_name: str):
        """Helper method to get a database collection."""
        from ...DB.database import get_database
        db = await get_database()
        return db[collection_name] 