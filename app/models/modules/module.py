from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field
from ..base import BaseDBModel, StatusModel

class ModuleStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class ModuleDifficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class ModuleObjective(BaseModel):
    title: str
    description: str

class ModuleCreate(BaseModel):
    title: str
    description: str
    order: int
    course_id: str
    estimated_duration: int  # in minutes
    difficulty: ModuleDifficulty
    objectives: List[ModuleObjective] = Field(default_factory=list)
    prerequisites: List[str] = Field(default_factory=list)  # List of module IDs

class Module(BaseDBModel, StatusModel):
    title: str
    description: str
    order: int
    course_id: str
    estimated_duration: int  # in minutes
    difficulty: ModuleDifficulty
    objectives: List[ModuleObjective] = Field(default_factory=list)
    prerequisites: List[str] = Field(default_factory=list)  # List of module IDs
    status: ModuleStatus = ModuleStatus.DRAFT
    lesson_ids: List[str] = Field(default_factory=list)
    assessment_ids: List[str] = Field(default_factory=list)
    completion_percentage: float = 0.0
    total_students_enrolled: int = 0
    average_completion_time: Optional[int] = None  # in minutes

    class Config:
        schema_extra = {
            "example": {
                "title": "Python Basics",
                "description": "Learn the fundamentals of Python programming",
                "order": 1,
                "course_id": "12345",
                "estimated_duration": 120,
                "difficulty": "easy",
                "objectives": [
                    {
                        "title": "Variables and Data Types",
                        "description": "Understanding Python variables and basic data types"
                    }
                ],
                "prerequisites": [],
                "status": "draft"
            }
        }

class ModuleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None
    estimated_duration: Optional[int] = None
    difficulty: Optional[ModuleDifficulty] = None
    objectives: Optional[List[ModuleObjective]] = None
    prerequisites: Optional[List[str]] = None
    status: Optional[ModuleStatus] = None 