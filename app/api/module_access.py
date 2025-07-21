from typing import Dict, Any
from fastapi import APIRouter, HTTPException, status, Query
from ..services.module_access_service import ModuleAccessService

router = APIRouter(prefix="/module-access", tags=["module-access"])
module_access_service = ModuleAccessService()

@router.get("/check/{student_email}/{course_id}/{module_id}", response_model=Dict[str, Any])
async def check_module_access(
    student_email: str,
    course_id: str,
    module_id: str
) -> Dict[str, Any]:
    """
    Check if a student has access to a specific module based on prerequisites and grades.
    
    Args:
        student_email: Student's email address
        course_id: Course ID
        module_id: Module ID to check access for
        
    Returns:
        Dict containing access status, reason, and grade information
    """
    try:
        access_info = await module_access_service.check_module_access(
            student_email, course_id, module_id
        )
        return access_info
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking module access: {str(e)}"
        )

@router.get("/course/{student_email}/{course_id}", response_model=Dict[str, Any])
async def get_course_module_access(
    student_email: str,
    course_id: str
) -> Dict[str, Any]:
    """
    Get access status for all modules in a course for a specific student.
    
    Args:
        student_email: Student's email address
        course_id: Course ID
        
    Returns:
        Dict containing access status for each module in the course
    """
    try:
        access_info = await module_access_service.get_student_module_access_for_course(
            student_email, course_id
        )
        return access_info
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting course module access: {str(e)}"
        )

@router.get("/python-module2/{student_email}", response_model=Dict[str, Any])
async def check_python_module2_access(student_email: str) -> Dict[str, Any]:
    """
    Check if a student has access to Python Module 2 based on Assessment1 grade.
    This endpoint matches your current frontend logic.
    
    Args:
        student_email: Student's email address
        
    Returns:
        Dict containing access status and grade information
    """
    try:
        has_access = await module_access_service.check_python_module2_access(student_email)
        
        # Get the actual grade for more detailed response
        grade_record = module_access_service.grades_service.get_grades_by_token(
            student_email, "Assessment1"
        )
        
        current_grade = grade_record.get("grade", 0.0) if grade_record else 0.0
        
        return {
            "has_access": has_access,
            "module_id": "python-module2",
            "prerequisite_assessment": "Assessment1",
            "required_grade": 40.0,
            "current_grade": current_grade,
            "reason": f"Assessment1 grade: {current_grade}/40.0" if grade_record else "No Assessment1 grade found"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking Python Module 2 access: {str(e)}"
        ) 