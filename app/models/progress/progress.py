from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from ..base import BaseDBModel

class ContentType(str, Enum):
    LESSON = "lesson"
    ASSESSMENT = "assessment"

class ProgressStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class ContentProgress(BaseModel):
    status: ProgressStatus = ProgressStatus.NOT_STARTED
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    time_spent_seconds: int = 0
    last_position: Optional[Dict[str, Any]] = None  # For storing content-specific progress data

class ModuleProgress(BaseModel):
    module_id: str
    status: ProgressStatus = ProgressStatus.NOT_STARTED
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    content_progress: Dict[str, ContentProgress] = Field(default_factory=dict)  # content_id -> progress

class CourseProgress(BaseDBModel):
    user_id: str
    course_id: str
    status: ProgressStatus = ProgressStatus.NOT_STARTED
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    module_progress: Dict[str, ModuleProgress] = Field(default_factory=dict)  # module_id -> progress
    last_accessed_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        schema_extra = {
            "example": {
                "user_id": "user123",
                "course_id": "course456",
                "status": "in_progress",
                "started_at": "2024-03-20T10:00:00Z",
                "module_progress": {
                    "module789": {
                        "module_id": "module789",
                        "status": "in_progress",
                        "started_at": "2024-03-20T10:00:00Z",
                        "content_progress": {
                            "lesson123": {
                                "status": "completed",
                                "started_at": "2024-03-20T10:00:00Z",
                                "completed_at": "2024-03-20T10:30:00Z",
                                "time_spent_seconds": 1800,
                                "last_position": {"section": 3, "completed": True}
                            }
                        }
                    }
                }
            }
        } 