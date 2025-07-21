from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, Query
from ..models.lessons.lesson import Lesson, LessonCreate, LessonUpdate, LessonStatus
from ..services.lessons.lesson_service import LessonService
from ..core.auth import get_current_user_payload, require_instructor, require_student

router = APIRouter(prefix="/lessons", tags=["lessons"])
lesson_service = LessonService()

@router.post("", response_model=Lesson)
async def create_lesson(
    lesson: LessonCreate,
    user_payload: Dict[str, Any] = Depends(require_instructor)
) -> Lesson:
    """Create a new lesson."""
    return await lesson_service.create_lesson(lesson)

@router.get("/{lesson_id}", response_model=Lesson)
async def get_lesson(
    lesson_id: str,
    user_payload: Dict[str, Any] = Depends(require_student)
) -> Lesson:
    """Get a lesson by ID."""
    lesson = await lesson_service.get_lesson(lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson

@router.get("/module/{module_id}", response_model=List[Lesson])
async def list_module_lessons(
    module_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    include_archived: bool = Query(False),
    user_payload: Dict[str, Any] = Depends(require_student)
) -> List[Lesson]:
    """List all lessons in a module."""
    return await lesson_service.list_lessons(
        module_id=module_id,
        skip=skip,
        limit=limit,
        include_archived=include_archived
    )

@router.put("/{lesson_id}", response_model=Lesson)
async def update_lesson(
    lesson_id: str,
    lesson_update: LessonUpdate,
    user_payload: Dict[str, Any] = Depends(require_instructor)
) -> Lesson:
    """Update a lesson."""
    updated_lesson = await lesson_service.update_lesson(lesson_id, lesson_update)
    if not updated_lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return updated_lesson

@router.delete("/{lesson_id}")
async def delete_lesson(
    lesson_id: str,
    user_payload: Dict[str, Any] = Depends(require_instructor)
) -> dict:
    """Delete a lesson."""
    success = await lesson_service.delete_lesson(lesson_id)
    if not success:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return {"message": "Lesson deleted successfully"}

@router.put("/{lesson_id}/sequence", response_model=Lesson)
async def update_lesson_sequence(
    lesson_id: str,
    next_lesson_id: Optional[str] = Query(None),
    previous_lesson_id: Optional[str] = Query(None),
    user_payload: Dict[str, Any] = Depends(require_instructor)
) -> Lesson:
    """Update the lesson sequence."""
    updated_lesson = await lesson_service.update_lesson_sequence(
        lesson_id=lesson_id,
        next_lesson_id=next_lesson_id,
        previous_lesson_id=previous_lesson_id
    )
    if not updated_lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return updated_lesson

@router.put("/{lesson_id}/metrics", response_model=Lesson)
async def update_lesson_metrics(
    lesson_id: str,
    total_views: Optional[int] = Query(None, ge=0),
    average_time_spent: Optional[int] = Query(None, ge=0),
    completion_count: Optional[int] = Query(None, ge=0),
    user_payload: Dict[str, Any] = Depends(require_instructor)
) -> Lesson:
    """Update lesson metrics."""
    updated_lesson = await lesson_service.update_lesson_metrics(
        lesson_id=lesson_id,
        total_views=total_views,
        average_time_spent=average_time_spent,
        completion_count=completion_count
    )
    if not updated_lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return updated_lesson

@router.put("/{lesson_id}/status", response_model=Lesson)
async def update_lesson_status(
    lesson_id: str,
    status: LessonStatus,
    user_payload: Dict[str, Any] = Depends(require_instructor)
) -> Lesson:
    """Update lesson status (draft/published/archived)."""
    lesson_update = LessonUpdate(status=status)
    updated_lesson = await lesson_service.update_lesson(lesson_id, lesson_update)
    if not updated_lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return updated_lesson 