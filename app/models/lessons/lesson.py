from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field
from ..base import BaseDBModel, StatusModel

class ContentType(str, Enum):
    TEXT = "text"
    CODE = "code"
    EXERCISE = "exercise"
    IMAGE = "image"

class LessonStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class CodeContent(BaseModel):
    language: str
    code: str
    explanation: Optional[str] = None

class ExerciseTestCase(BaseModel):
    input: str
    expected_output: str
    explanation: Optional[str] = None

class InteractiveExercise(BaseModel):
    instructions: str
    initial_code: str
    language: str
    test_cases: List[ExerciseTestCase]
    hints: List[str] = Field(default_factory=list)
    solution: Optional[str] = None

class ImageContent(BaseModel):
    url: str
    alt_text: str
    caption: Optional[str] = None

class Content(BaseModel):
    type: ContentType
    order: int
    content: Dict[str, Any]  # Will contain different content based on type

class LessonCreate(BaseModel):
    title: str
    description: str
    order: int
    module_id: str
    course_id: str
    estimated_duration: int  # in minutes
    content_blocks: List[Content] = Field(default_factory=list)

class Lesson(BaseDBModel, StatusModel):
    title: str
    description: str
    order: int
    module_id: str
    course_id: str
    estimated_duration: int  # in minutes
    content_blocks: List[Content] = Field(default_factory=list)
    status: LessonStatus = LessonStatus.DRAFT
    next_lesson_id: Optional[str] = None
    previous_lesson_id: Optional[str] = None
    total_views: int = 0
    average_time_spent: Optional[int] = None  # in minutes
    completion_count: int = 0

    class Config:
        schema_extra = {
            "example": {
                "title": "Introduction to Variables",
                "description": "Learn about Python variables and their usage",
                "order": 1,
                "module_id": "12345",
                "course_id": "67890",
                "estimated_duration": 30,
                "content_blocks": [
                    {
                        "type": "text",
                        "order": 1,
                        "content": {
                            "text": "Variables are containers for storing data values..."
                        }
                    },
                    {
                        "type": "code",
                        "order": 2,
                        "content": {
                            "language": "python",
                            "code": "x = 5\nprint(x)",
                            "explanation": "This code demonstrates variable assignment"
                        }
                    }
                ],
                "status": "draft"
            }
        }

class LessonUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None
    estimated_duration: Optional[int] = None
    content_blocks: Optional[List[Content]] = None
    status: Optional[LessonStatus] = None
    next_lesson_id: Optional[str] = None
    previous_lesson_id: Optional[str] = None 