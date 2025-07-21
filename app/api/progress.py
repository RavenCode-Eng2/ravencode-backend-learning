from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, Query
from ..models.progress.progress import CourseProgress, ContentType
from ..services.progress.progress_service import ProgressService
from ..core.auth import get_current_user_payload, require_student

router = APIRouter(prefix="/progress", tags=["progress"])
progress_service = ProgressService()

@router.get("/courses/{course_id}", response_model=CourseProgress)
async def get_course_progress(
    course_id: str,
    user_payload: Dict[str, Any] = Depends(require_student)
) -> CourseProgress:
    """Get the user's progress in a specific course."""
    progress = await progress_service.get_course_progress(
        user_id=user_payload["user_id"],
        course_id=course_id
    )
    if not progress:
        # Initialize progress if it doesn't exist
        progress = await progress_service.initialize_course_progress(
            user_id=user_payload["user_id"],
            course_id=course_id
        )
    return progress

@router.get("/courses", response_model=List[CourseProgress])
async def list_user_progress(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    user_payload: Dict[str, Any] = Depends(require_student)
) -> List[CourseProgress]:
    """List progress in all courses for the current user."""
    return await progress_service.list_user_progress(
        user_id=user_payload["user_id"],
        skip=skip,
        limit=limit
    )

@router.post("/courses/{course_id}/modules/{module_id}/content/{content_id}")
async def update_content_progress(
    course_id: str,
    module_id: str,
    content_id: str,
    content_type: ContentType,
    time_spent: int = Query(..., ge=0),  # Required, must be non-negative
    completed: bool = Query(False),
    last_position: Dict[str, Any] = None,
    user_payload: Dict[str, Any] = Depends(require_student)
) -> CourseProgress:
    """Update progress for a specific content item (lesson or assessment)."""
    updated_progress = await progress_service.update_content_progress(
        user_id=user_payload["user_id"],
        course_id=course_id,
        module_id=module_id,
        content_id=content_id,
        content_type=content_type,
        time_spent=time_spent,
        last_position=last_position,
        completed=completed
    )
    if not updated_progress:
        raise HTTPException(status_code=404, detail="Progress not found")
    return updated_progress 