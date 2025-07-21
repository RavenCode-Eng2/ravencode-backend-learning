from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field
from ..base import BaseDBModel, StatusModel

class CourseLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class CourseStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class CourseMetrics(BaseModel):
    total_students: int = 0
    average_rating: float = 0.0
    total_ratings: int = 0
    completion_rate: float = 0.0

class CourseObjective(BaseModel):
    title: str
    description: str

class CourseCreate(BaseModel):
    title: str
    description: str
    language: str
    level: CourseLevel
    category: str
    tags: List[str] = Field(default_factory=list)
    estimated_duration: int  # in minutes
    objectives: List[CourseObjective] = Field(default_factory=list)
    instructor_id: str
    
class Course(BaseDBModel, StatusModel):
    title: str
    description: str
    language: str
    level: CourseLevel
    category: str
    tags: List[str] = Field(default_factory=list)
    estimated_duration: int  # in minutes
    objectives: List[CourseObjective] = Field(default_factory=list)
    instructor_id: str
    status: CourseStatus = CourseStatus.DRAFT
    metrics: CourseMetrics = Field(default_factory=CourseMetrics)
    module_ids: List[str] = Field(default_factory=list)
    
    class Config:
        schema_extra = {
            "example": {
                "title": "Introduction to Python Programming",
                "description": "A comprehensive course for beginners to learn Python",
                "language": "en",
                "level": "beginner",
                "category": "Programming",
                "tags": ["python", "programming", "beginner"],
                "estimated_duration": 1800,
                "objectives": [
                    {
                        "title": "Learn Python Basics",
                        "description": "Understand basic Python syntax and data types"
                    }
                ],
                "instructor_id": "12345",
                "status": "draft"
            }
        }

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    language: Optional[str] = None
    level: Optional[CourseLevel] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    estimated_duration: Optional[int] = None
    objectives: Optional[List[CourseObjective]] = None
    status: Optional[CourseStatus] = None 