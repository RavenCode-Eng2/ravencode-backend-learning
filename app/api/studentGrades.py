# src/api/studentGrades.py
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Dict, Any

from app.models.studentGrades import StudentGrades
from app.services.studentGrades import GradesService

router = APIRouter()

def get_student_grade_service():
    return GradesService()

@router.post(
    "/",
    response_model=Dict[str, Any],
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "description": "Grade created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Grade created successfully",
                        "grade": {
                            "email": "token123",
                            "module": "Math101",
                            "grade": 95.0,
                            "date_assigned": "2025-06-08"
                        }
                    }
                }
            }
        },
        400: {"description": "Grade already exists or invalid data"}
    }
)
async def create_grade(grade: StudentGrades, service: GradesService = Depends(get_student_grade_service)):
    """
    Create or update a student's grade in the database.
    If the student already has grades, updates them.
    """
    try:
        # Llamamos al servicio que maneja la creación  de las calificaciones
        result = service.create_grade(grade)
        return {
            "grade": result  # Aquí result debe ser lo que retorna el servicio
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.patch(
    "/{email}/{module}",
    response_model=Dict[str, Any],
    responses={
        200: {
            "description": "Grade updated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Grade updated successfully",
                        "grade": {
                            "email": "token123",
                            "module": "Math101",
                            "grade": 97.0,
                            "date_assigned": "2025-06-08"
                        }
                    }
                }
            }
        },
        404: {"description": "Grade not found"},
        400: {"description": "Invalid data"}
    }
)
async def update_grade(email: str, module: str, grade: StudentGrades, service: GradesService = Depends(get_student_grade_service)):
    """
    Update an existing grade for the student.
    """
    try:
        # Actualiza la calificación existente para el estudiante
        result = service.update_grades(grade)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/{email}/{module}",
    response_model=Dict[str, Any],
    responses={
        200: {
            "description": "Grade found",
            "content": {
                "application/json": {
                    "example": {
                        "email": "token123",
                        "module": "Math101",
                        "grade": 95.0,
                        "date_assigned": "2025-06-08"
                    }
                }
            }
        },
        404: {"description": "Grade not found"}
    }
)
async def get_grade(email: str, module: str, service: GradesService = Depends(get_student_grade_service)):
    try:
        grade = service.get_grades_by_email(email, module)
        if not grade:
            raise HTTPException(status_code=404, detail="Grade not found")
        return grade
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get(
    "/",
    response_model=List[Dict[str, Any]],
    responses={
        200: {
            "description": "List of all grades",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "email": "token123",
                            "module": "Math101",
                            "grade": 95.0,
                            "date_assigned": "2025-06-08"
                        }
                    ]
                }
            }
        }
    }
)
async def list_grades(service: GradesService = Depends(get_student_grade_service)):
    try:
        return service.list_grades()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
