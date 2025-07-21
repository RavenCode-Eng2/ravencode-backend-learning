from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, status, Query
from ..models.roadmaps.roadmap import (
    Roadmap, RoadmapCreate, RoadmapUpdate, 
    RoadmapStatus, RoadmapCategory, RoadmapDifficulty
)
from ..services.roadmaps.roadmap_service import RoadmapService

router = APIRouter(prefix="/roadmaps", tags=["roadmaps"])
roadmap_service = RoadmapService()

@router.post("", response_model=Roadmap, status_code=status.HTTP_201_CREATED)
async def create_roadmap(roadmap_data: RoadmapCreate) -> Roadmap:
    """
    Create a new roadmap.
    """
    try:
        return await roadmap_service.create_roadmap(roadmap_data)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creating roadmap: {str(e)}"
        )

@router.get("", response_model=List[Roadmap])
async def list_roadmaps(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    category: Optional[RoadmapCategory] = None,
    difficulty: Optional[RoadmapDifficulty] = None,
    status: Optional[RoadmapStatus] = None,
    instructor_id: Optional[str] = None,
    search_term: Optional[str] = None
) -> List[Roadmap]:
    """
    List roadmaps with filtering and search options.
    """
    try:
        return await roadmap_service.list_roadmaps(
            skip=skip,
            limit=limit,
            category=category,
            difficulty=difficulty,
            status=status,
            instructor_id=instructor_id,
            search_term=search_term
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error listing roadmaps: {str(e)}"
        )

@router.get("/published", response_model=List[Roadmap])
async def get_published_roadmaps() -> List[Roadmap]:
    """
    Get all published roadmaps.
    """
    try:
        return await roadmap_service.get_published_roadmaps()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting published roadmaps: {str(e)}"
        )

@router.get("/category/{category}", response_model=List[Roadmap])
async def get_roadmaps_by_category(category: RoadmapCategory) -> List[Roadmap]:
    """
    Get all roadmaps in a specific category.
    """
    try:
        return await roadmap_service.get_roadmaps_by_category(category)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting roadmaps by category: {str(e)}"
        )

@router.get("/instructor/{instructor_id}", response_model=List[Roadmap])
async def get_roadmaps_by_instructor(instructor_id: str) -> List[Roadmap]:
    """
    Get all roadmaps created by a specific instructor.
    """
    try:
        return await roadmap_service.get_roadmaps_by_instructor(instructor_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting roadmaps by instructor: {str(e)}"
        )

@router.get("/{roadmap_id}", response_model=Roadmap)
async def get_roadmap(roadmap_id: str) -> Roadmap:
    """
    Get a roadmap by ID.
    """
    try:
        roadmap = await roadmap_service.get_roadmap(roadmap_id)
        if not roadmap:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Roadmap not found"
            )
        return roadmap
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting roadmap: {str(e)}"
        )

@router.get("/{roadmap_id}/detailed", response_model=Dict[str, Any])
async def get_roadmap_with_course_details(roadmap_id: str) -> Dict[str, Any]:
    """
    Get a roadmap with detailed course information.
    """
    try:
        roadmap_details = await roadmap_service.get_roadmap_with_courses_details(roadmap_id)
        if not roadmap_details:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Roadmap not found"
            )
        return roadmap_details
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting roadmap details: {str(e)}"
        )

@router.put("/{roadmap_id}", response_model=Roadmap)
async def update_roadmap(roadmap_id: str, roadmap_update: RoadmapUpdate) -> Roadmap:
    """
    Update a roadmap.
    """
    try:
        updated_roadmap = await roadmap_service.update_roadmap(roadmap_id, roadmap_update)
        if not updated_roadmap:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Roadmap not found"
            )
        return updated_roadmap
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating roadmap: {str(e)}"
        )

@router.delete("/{roadmap_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_roadmap(roadmap_id: str):
    """
    Delete a roadmap.
    """
    try:
        success = await roadmap_service.delete_roadmap(roadmap_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Roadmap not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting roadmap: {str(e)}"
        )

@router.get("/{roadmap_id}/progress/{student_email}", response_model=Dict[str, Any])
async def get_student_roadmap_progress(roadmap_id: str, student_email: str) -> Dict[str, Any]:
    """
    Get a student's progress through a roadmap.
    """
    try:
        progress = await roadmap_service.get_student_roadmap_progress(student_email, roadmap_id)
        if "error" in progress:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=progress["error"]
            )
        return progress
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting student progress: {str(e)}"
        )

@router.post("/{roadmap_id}/courses", response_model=Roadmap)
async def add_course_to_roadmap(
    roadmap_id: str, 
    course_data: Dict[str, Any]
) -> Roadmap:
    """
    Add a course to a roadmap.
    """
    try:
        updated_roadmap = await roadmap_service.add_course_to_roadmap(roadmap_id, course_data)
        if not updated_roadmap:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Roadmap not found"
            )
        return updated_roadmap
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding course to roadmap: {str(e)}"
        )

@router.delete("/{roadmap_id}/courses/{course_id}", response_model=Roadmap)
async def remove_course_from_roadmap(roadmap_id: str, course_id: str) -> Roadmap:
    """
    Remove a course from a roadmap.
    """
    try:
        updated_roadmap = await roadmap_service.remove_course_from_roadmap(roadmap_id, course_id)
        if not updated_roadmap:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Roadmap not found"
            )
        return updated_roadmap
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error removing course from roadmap: {str(e)}"
        )

# Frontend-specific endpoints for easier integration
@router.get("/frontend/categories", response_model=List[Dict[str, Any]])
async def get_roadmap_categories() -> List[Dict[str, Any]]:
    """
    Get all available roadmap categories for frontend display.
    """
    return [
        {"value": "web_development", "label": "Web Development", "description": "Frontend and backend web development"},
        {"value": "mobile_development", "label": "Mobile Development", "description": "iOS and Android app development"},
        {"value": "data_science", "label": "Data Science", "description": "Data analysis and visualization"},
        {"value": "machine_learning", "label": "Machine Learning", "description": "AI and ML model development"},
        {"value": "devops", "label": "DevOps", "description": "Infrastructure and deployment automation"},
        {"value": "cybersecurity", "label": "Cybersecurity", "description": "Security and ethical hacking"},
        {"value": "game_development", "label": "Game Development", "description": "Video game creation"},
        {"value": "blockchain", "label": "Blockchain", "description": "Cryptocurrency and blockchain technology"},
        {"value": "cloud_computing", "label": "Cloud Computing", "description": "Cloud platforms and services"},
        {"value": "ai_development", "label": "AI Development", "description": "Artificial intelligence development"}
    ]

@router.get("/frontend/featured", response_model=List[Dict[str, Any]])
async def get_featured_roadmaps() -> List[Dict[str, Any]]:
    """
    Get featured roadmaps for frontend display with mock data.
    """
    # Mock data for featured roadmaps
    return [
        {
            "id": "web-dev-roadmap",
            "title": "Full Stack Web Development",
            "description": "Complete roadmap to become a full stack web developer",
            "category": "web_development",
            "difficulty": "intermediate",
            "estimated_duration_weeks": 24,
            "image_url": "https://via.placeholder.com/400x200?text=Web+Development",
            "total_courses": 6,
            "enrolled_students": 1250,
            "rating": 4.8,
            "skills": ["HTML", "CSS", "JavaScript", "React", "Node.js", "MongoDB"]
        },
        {
            "id": "data-science-roadmap",
            "title": "Data Science Mastery",
            "description": "From beginner to data science expert",
            "category": "data_science",
            "difficulty": "intermediate",
            "estimated_duration_weeks": 20,
            "image_url": "https://via.placeholder.com/400x200?text=Data+Science",
            "total_courses": 5,
            "enrolled_students": 890,
            "rating": 4.7,
            "skills": ["Python", "Pandas", "NumPy", "Matplotlib", "Scikit-learn", "SQL"]
        },
        {
            "id": "ml-roadmap",
            "title": "Machine Learning Engineer",
            "description": "Build and deploy ML models in production",
            "category": "machine_learning",
            "difficulty": "advanced",
            "estimated_duration_weeks": 28,
            "image_url": "https://via.placeholder.com/400x200?text=Machine+Learning",
            "total_courses": 7,
            "enrolled_students": 650,
            "rating": 4.9,
            "skills": ["Python", "TensorFlow", "PyTorch", "MLOps", "Docker", "Kubernetes"]
        }
    ] 