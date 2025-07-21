from typing import List, Optional, Dict, Any
from ...DB.database import get_database
from ...models.roadmaps.roadmap import Roadmap, RoadmapCreate, RoadmapUpdate, RoadmapStatus, RoadmapCategory, RoadmapDifficulty
from ..base import BaseService

class RoadmapService(BaseService):
    """
    Service for managing roadmaps in the database.
    """
    
    def __init__(self):
        super().__init__("roadmaps")
    
    async def create_roadmap(self, roadmap: RoadmapCreate) -> Roadmap:
        """Create a new roadmap."""
        roadmap_dict = await self.create(roadmap)
        return Roadmap.model_validate(roadmap_dict)
    
    async def get_roadmap(self, roadmap_id: str) -> Optional[Roadmap]:
        """Get a roadmap by ID."""
        roadmap_dict = await self.get_by_id(roadmap_id)
        return Roadmap.model_validate(roadmap_dict) if roadmap_dict else None
    
    async def list_roadmaps(
        self,
        skip: int = 0,
        limit: int = 10,
        category: Optional[RoadmapCategory] = None,
        difficulty: Optional[RoadmapDifficulty] = None,
        status: Optional[RoadmapStatus] = None,
        instructor_id: Optional[str] = None,
        search_term: Optional[str] = None
    ) -> List[Roadmap]:
        """List roadmaps with filtering and search."""
        filter_query: Dict[str, Any] = {}
        
        if category:
            filter_query["category"] = category
        if difficulty:
            filter_query["difficulty"] = difficulty
        if status:
            filter_query["status"] = status
        if instructor_id:
            filter_query["instructor_id"] = instructor_id
        if search_term:
            filter_query["$or"] = [
                {"title": {"$regex": search_term, "$options": "i"}},
                {"description": {"$regex": search_term, "$options": "i"}},
                {"tags": {"$in": [search_term]}}
            ]
        
        roadmaps = await self.get_all(skip=skip, limit=limit, filter_query=filter_query)
        return [Roadmap.model_validate(roadmap) for roadmap in roadmaps]
    
    async def update_roadmap(self, roadmap_id: str, roadmap_update: RoadmapUpdate) -> Optional[Roadmap]:
        """Update a roadmap."""
        roadmap_dict = await self.update(roadmap_id, roadmap_update)
        return Roadmap.model_validate(roadmap_dict) if roadmap_dict else None
    
    async def delete_roadmap(self, roadmap_id: str) -> bool:
        """Delete a roadmap."""
        return await self.delete(roadmap_id)
    
    async def get_roadmaps_by_category(self, category: RoadmapCategory) -> List[Roadmap]:
        """Get all roadmaps in a specific category."""
        return await self.list_roadmaps(category=category, status=RoadmapStatus.PUBLISHED, limit=100)
    
    async def get_published_roadmaps(self) -> List[Roadmap]:
        """Get all published roadmaps."""
        return await self.list_roadmaps(status=RoadmapStatus.PUBLISHED, limit=100)
    
    async def get_roadmaps_by_instructor(self, instructor_id: str) -> List[Roadmap]:
        """Get all roadmaps created by a specific instructor."""
        return await self.list_roadmaps(instructor_id=instructor_id, limit=100)
    
    async def add_course_to_roadmap(self, roadmap_id: str, course_roadmap_data: Dict[str, Any]) -> Optional[Roadmap]:
        """Add a course to a roadmap."""
        collection = await self.get_collection()
        result = await collection.update_one(
            {"_id": roadmap_id},
            {"$push": {"courses": course_roadmap_data}}
        )
        if result.modified_count == 0:
            return None
        return await self.get_roadmap(roadmap_id)
    
    async def remove_course_from_roadmap(self, roadmap_id: str, course_id: str) -> Optional[Roadmap]:
        """Remove a course from a roadmap."""
        collection = await self.get_collection()
        result = await collection.update_one(
            {"_id": roadmap_id},
            {"$pull": {"courses": {"course_id": course_id}}}
        )
        if result.modified_count == 0:
            return None
        return await self.get_roadmap(roadmap_id)
    
    async def update_roadmap_metrics(
        self,
        roadmap_id: str,
        total_enrolled: Optional[int] = None,
        total_completed: Optional[int] = None,
        average_completion_time_weeks: Optional[float] = None,
        completion_rate: Optional[float] = None,
        average_rating: Optional[float] = None,
        total_ratings: Optional[int] = None
    ) -> Optional[Roadmap]:
        """Update roadmap metrics."""
        update_data: Dict[str, Any] = {}
        
        if total_enrolled is not None:
            update_data["metrics.total_enrolled"] = total_enrolled
        if total_completed is not None:
            update_data["metrics.total_completed"] = total_completed
        if average_completion_time_weeks is not None:
            update_data["metrics.average_completion_time_weeks"] = average_completion_time_weeks
        if completion_rate is not None:
            update_data["metrics.completion_rate"] = completion_rate
        if average_rating is not None:
            update_data["metrics.average_rating"] = average_rating
        if total_ratings is not None:
            update_data["metrics.total_ratings"] = total_ratings
            
        if not update_data:
            return await self.get_roadmap(roadmap_id)
            
        collection = await self.get_collection()
        result = await collection.update_one(
            {"_id": roadmap_id},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            return None
            
        return await self.get_roadmap(roadmap_id)
    
    async def get_roadmap_with_courses_details(self, roadmap_id: str) -> Optional[Dict[str, Any]]:
        """Get a roadmap with detailed course information."""
        from ...DB.database import get_database
        
        roadmap = await self.get_roadmap(roadmap_id)
        if not roadmap:
            return None
        
        # Get course details for each course in the roadmap
        db = await get_database()
        courses_collection = db["courses"]
        
        detailed_courses = []
        for course_in_roadmap in roadmap.courses:
            course_detail = await courses_collection.find_one({"_id": course_in_roadmap.course_id})
            if course_detail:
                detailed_courses.append({
                    "roadmap_info": course_in_roadmap.model_dump(),
                    "course_details": {
                        "id": str(course_detail["_id"]),
                        "title": course_detail.get("title", ""),
                        "description": course_detail.get("description", ""),
                        "level": course_detail.get("level", ""),
                        "estimated_duration": course_detail.get("estimated_duration", 0),
                        "status": course_detail.get("status", "")
                    }
                })
        
        return {
            "roadmap": roadmap.model_dump(),
            "courses": detailed_courses
        }
    
    async def get_student_roadmap_progress(self, student_email: str, roadmap_id: str) -> Dict[str, Any]:
        """Get a student's progress through a roadmap."""
        from ..studentGrades import GradesService
        
        roadmap = await self.get_roadmap(roadmap_id)
        if not roadmap:
            return {"error": "Roadmap not found"}
        
        grades_service = GradesService()
        course_progress = {}
        total_courses = len(roadmap.courses)
        completed_courses = 0
        
        for course_in_roadmap in roadmap.courses:
            course_id = course_in_roadmap.course_id
            
            # Check if student has completed this course
            # This is a simplified check - you might want to implement more sophisticated logic
            grade_record = grades_service.get_grades_by_token(student_email, f"{course_id}-final")
            
            if grade_record and grade_record.get("grade", 0) >= 40:
                course_progress[course_id] = {
                    "completed": True,
                    "grade": grade_record.get("grade"),
                    "completion_date": grade_record.get("date_assigned")
                }
                completed_courses += 1
            else:
                course_progress[course_id] = {
                    "completed": False,
                    "grade": grade_record.get("grade") if grade_record else None,
                    "completion_date": None
                }
        
        progress_percentage = (completed_courses / total_courses * 100) if total_courses > 0 else 0
        
        return {
            "roadmap_id": roadmap_id,
            "student_email": student_email,
            "progress_percentage": progress_percentage,
            "completed_courses": completed_courses,
            "total_courses": total_courses,
            "course_progress": course_progress,
            "roadmap_completed": completed_courses == total_courses
        } 