from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime
from ..base import BaseDBModel, StatusModel

class RoadmapStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class RoadmapDifficulty(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class RoadmapCategory(str, Enum):
    WEB_DEVELOPMENT = "web_development"
    MOBILE_DEVELOPMENT = "mobile_development"
    DATA_SCIENCE = "data_science"
    MACHINE_LEARNING = "machine_learning"
    DEVOPS = "devops"
    CYBERSECURITY = "cybersecurity"
    GAME_DEVELOPMENT = "game_development"
    BLOCKCHAIN = "blockchain"
    CLOUD_COMPUTING = "cloud_computing"
    AI_DEVELOPMENT = "ai_development"

class CourseInRoadmap(BaseModel):
    """
    Represents a course within a roadmap with its position and requirements.
    """
    course_id: str = Field(..., description="ID of the course")
    order: int = Field(..., description="Order of the course in the roadmap (1-based)")
    is_required: bool = Field(True, description="Whether this course is required or optional")
    prerequisites: List[str] = Field(default_factory=list, description="List of course IDs that must be completed before this course")
    estimated_duration_weeks: int = Field(..., description="Estimated duration in weeks to complete this course")
    description: Optional[str] = Field(None, description="Description of why this course is in the roadmap")

class RoadmapMilestone(BaseModel):
    """
    Represents a milestone in the roadmap that groups related courses.
    """
    id: str = Field(..., description="Unique identifier for the milestone")
    title: str = Field(..., description="Title of the milestone")
    description: str = Field(..., description="Description of what will be achieved")
    order: int = Field(..., description="Order of the milestone in the roadmap")
    course_ids: List[str] = Field(default_factory=list, description="List of course IDs in this milestone")
    estimated_duration_weeks: int = Field(..., description="Estimated duration to complete this milestone")

class RoadmapSkill(BaseModel):
    """
    Represents a skill that will be learned in the roadmap.
    """
    name: str = Field(..., description="Name of the skill")
    description: str = Field(..., description="Description of the skill")
    level: str = Field(..., description="Level of proficiency (beginner, intermediate, advanced)")

class RoadmapCareerPath(BaseModel):
    """
    Represents career opportunities after completing the roadmap.
    """
    title: str = Field(..., description="Job title or career path")
    description: str = Field(..., description="Description of the career path")
    average_salary_range: Optional[str] = Field(None, description="Average salary range for this career")
    required_skills: List[str] = Field(default_factory=list, description="Key skills required for this career")

class RoadmapMetrics(BaseModel):
    """
    Metrics and statistics for the roadmap.
    """
    total_enrolled: int = Field(default=0, description="Total number of students enrolled")
    total_completed: int = Field(default=0, description="Total number of students who completed the roadmap")
    average_completion_time_weeks: Optional[float] = Field(default=None, description="Average time to complete in weeks")
    completion_rate: float = Field(default=0.0, description="Percentage of students who complete the roadmap")
    average_rating: float = Field(default=0.0, description="Average rating from students")
    total_ratings: int = Field(default=0, description="Total number of ratings")

class RoadmapCreate(BaseModel):
    """
    Schema for creating a new roadmap.
    """
    title: str = Field(..., description="Title of the roadmap")
    description: str = Field(..., description="Detailed description of the roadmap")
    category: RoadmapCategory = Field(..., description="Category of the roadmap")
    difficulty: RoadmapDifficulty = Field(..., description="Overall difficulty level")
    estimated_duration_weeks: int = Field(..., description="Estimated total duration in weeks")
    instructor_id: str = Field(..., description="ID of the instructor who created the roadmap")
    courses: List[CourseInRoadmap] = Field(default_factory=list, description="List of courses in the roadmap")
    milestones: List[RoadmapMilestone] = Field(default_factory=list, description="List of milestones")
    skills_learned: List[RoadmapSkill] = Field(default_factory=list, description="Skills that will be learned")
    career_paths: List[RoadmapCareerPath] = Field(default_factory=list, description="Career opportunities")
    tags: List[str] = Field(default_factory=list, description="Tags for searching and categorization")
    image_url: Optional[str] = Field(None, description="URL of the roadmap image")

class RoadmapUpdate(BaseModel):
    """
    Schema for updating an existing roadmap.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[RoadmapCategory] = None
    difficulty: Optional[RoadmapDifficulty] = None
    estimated_duration_weeks: Optional[int] = None
    courses: Optional[List[CourseInRoadmap]] = None
    milestones: Optional[List[RoadmapMilestone]] = None
    skills_learned: Optional[List[RoadmapSkill]] = None
    career_paths: Optional[List[RoadmapCareerPath]] = None
    tags: Optional[List[str]] = None
    image_url: Optional[str] = None
    status: Optional[RoadmapStatus] = None

class Roadmap(BaseDBModel, StatusModel):
    """
    Complete roadmap model with all information.
    """
    title: str = Field(..., description="Title of the roadmap")
    description: str = Field(..., description="Detailed description of the roadmap")
    category: RoadmapCategory = Field(..., description="Category of the roadmap")
    difficulty: RoadmapDifficulty = Field(..., description="Overall difficulty level")
    estimated_duration_weeks: int = Field(..., description="Estimated total duration in weeks")
    instructor_id: str = Field(..., description="ID of the instructor who created the roadmap")
    courses: List[CourseInRoadmap] = Field(default_factory=list, description="List of courses in the roadmap")
    milestones: List[RoadmapMilestone] = Field(default_factory=list, description="List of milestones")
    skills_learned: List[RoadmapSkill] = Field(default_factory=list, description="Skills that will be learned")
    career_paths: List[RoadmapCareerPath] = Field(default_factory=list, description="Career opportunities")
    tags: List[str] = Field(default_factory=list, description="Tags for searching and categorization")
    image_url: Optional[str] = Field(None, description="URL of the roadmap image")
    status: RoadmapStatus = Field(RoadmapStatus.DRAFT, description="Current status of the roadmap")
    metrics: RoadmapMetrics = Field(default_factory=lambda: RoadmapMetrics(), description="Roadmap metrics and statistics")

    class Config:
        schema_extra = {
            "example": {
                "title": "Full Stack Web Development",
                "description": "Complete roadmap to become a full stack web developer",
                "category": "web_development",
                "difficulty": "intermediate",
                "estimated_duration_weeks": 24,
                "instructor_id": "instructor123",
                "courses": [
                    {
                        "course_id": "html-css-basics",
                        "order": 1,
                        "is_required": True,
                        "prerequisites": [],
                        "estimated_duration_weeks": 3,
                        "description": "Learn the fundamentals of web development"
                    },
                    {
                        "course_id": "javascript-fundamentals",
                        "order": 2,
                        "is_required": True,
                        "prerequisites": ["html-css-basics"],
                        "estimated_duration_weeks": 4,
                        "description": "Master JavaScript programming"
                    }
                ],
                "milestones": [
                    {
                        "id": "frontend-basics",
                        "title": "Frontend Fundamentals",
                        "description": "Master the basics of frontend development",
                        "order": 1,
                        "course_ids": ["html-css-basics", "javascript-fundamentals"],
                        "estimated_duration_weeks": 7
                    }
                ],
                "skills_learned": [
                    {
                        "name": "HTML/CSS",
                        "description": "Create and style web pages",
                        "level": "intermediate"
                    },
                    {
                        "name": "JavaScript",
                        "description": "Programming language for web development",
                        "level": "intermediate"
                    }
                ],
                "career_paths": [
                    {
                        "title": "Frontend Developer",
                        "description": "Create user interfaces for web applications",
                        "average_salary_range": "$60,000 - $120,000",
                        "required_skills": ["HTML", "CSS", "JavaScript", "React"]
                    }
                ],
                "tags": ["web development", "frontend", "backend", "full stack"],
                "status": "published"
            }
        } 