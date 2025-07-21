from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, Query
from ..models.assessments.assessment import (
    Assessment,
    AssessmentCreate,
    AssessmentUpdate,
    AssessmentStatus
)
from ..services.assessments.assessment_service import AssessmentService
from ..core.auth import get_current_user_payload, require_instructor, require_student

router = APIRouter(prefix="/assessments", tags=["assessments"])
assessment_service = AssessmentService()

@router.post("", response_model=Assessment)
async def create_assessment(
    assessment: AssessmentCreate,
    user_payload: Dict[str, Any] = Depends(require_instructor)
) -> Assessment:
    """Create a new assessment."""
    return await assessment_service.create_assessment(assessment)

@router.get("/{assessment_id}", response_model=Assessment)
async def get_assessment(
    assessment_id: str,
    user_payload: Dict[str, Any] = Depends(require_student)
) -> Assessment:
    """Get an assessment by ID."""
    assessment = await assessment_service.get_assessment(assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return assessment

@router.get("/module/{module_id}", response_model=List[Assessment])
async def list_module_assessments(
    module_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    include_archived: bool = Query(False),
    user_payload: Dict[str, Any] = Depends(require_student)
) -> List[Assessment]:
    """List all assessments in a module."""
    return await assessment_service.list_assessments(
        module_id=module_id,
        skip=skip,
        limit=limit,
        include_archived=include_archived
    )

@router.put("/{assessment_id}", response_model=Assessment)
async def update_assessment(
    assessment_id: str,
    assessment_update: AssessmentUpdate,
    user_payload: Dict[str, Any] = Depends(require_instructor)
) -> Assessment:
    """Update an assessment."""
    updated_assessment = await assessment_service.update_assessment(assessment_id, assessment_update)
    if not updated_assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return updated_assessment

@router.delete("/{assessment_id}")
async def delete_assessment(
    assessment_id: str,
    user_payload: Dict[str, Any] = Depends(require_instructor)
) -> dict:
    """Delete an assessment."""
    success = await assessment_service.delete_assessment(assessment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return {"message": "Assessment deleted successfully"}

@router.put("/{assessment_id}/status", response_model=Assessment)
async def update_assessment_status(
    assessment_id: str,
    status: AssessmentStatus,
    user_payload: Dict[str, Any] = Depends(require_instructor)
) -> Assessment:
    """Update assessment status (draft/published/archived)."""
    assessment_update = AssessmentUpdate(status=status)
    updated_assessment = await assessment_service.update_assessment(assessment_id, assessment_update)
    if not updated_assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return updated_assessment 