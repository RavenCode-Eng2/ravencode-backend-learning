from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field
from ..base import BaseDBModel, StatusModel

class AssessmentType(str, Enum):
    CODING = "coding"
    QUIZ = "quiz"
    PROJECT = "project"

class AssessmentStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class AssessmentContent(BaseModel):
    """
    Generic content model that can hold any type of assessment content.
    The structure of the content will be validated by the evaluation service.
    """
    type: AssessmentType
    content: Dict[str, Any]  # Raw content to be validated by evaluation service
    metadata: Optional[Dict[str, Any]] = None  # Additional metadata specific to the assessment type

class AssessmentCreate(BaseModel):
    title: str
    description: str
    module_id: str
    course_id: str
    order: int
    content: AssessmentContent

class Assessment(BaseDBModel, StatusModel):
    title: str
    description: str
    module_id: str
    course_id: str
    order: int
    content: AssessmentContent
    status: AssessmentStatus = AssessmentStatus.DRAFT

    class Config:
        use_enum_values = True
        schema_extra = {
            "example": {
                "title": "Python Functions Quiz",
                "description": "Test your knowledge of Python functions",
                "module_id": "12345",
                "course_id": "67890",
                "order": 1,
                "content": {
                    "type": "quiz",
                    "content": {
                        "questions": [
                            {
                                "question": "What is a lambda function?",
                                "options": [
                                    {"text": "An anonymous function", "is_correct": True},
                                    {"text": "A Greek letter", "is_correct": False}
                                ]
                            }
                        ]
                    },
                    "metadata": {
                        "time_limit_minutes": 30,
                        "passing_score": 70
                    }
                },
                "status": "draft"
            }
        }

class AssessmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None
    content: Optional[AssessmentContent] = None
    status: Optional[AssessmentStatus] = None 