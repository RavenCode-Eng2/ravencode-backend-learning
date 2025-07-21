# src/api/studentResponses.py
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Dict, Any

from app.models.studentResponses import StudentResponses
from app.services.studentResponses import ResponsesService

router = APIRouter()

def get_student_responses_service():
    return ResponsesService()

@router.post(
    "/responses/",
    response_model=Dict[str, Any],
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "description": "Responses saved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Responses saved successfully",
                        "responses": {
                            "email": "token123",
                            "responses": [
                                {"question_id": "1", "response": "A"},
                                {"question_id": "2", "response": "B"}
                            ]
                        }
                    }
                }
            }
        },
        400: {"description": "Invalid responses data"}
    }
)
async def save_responses(responses: StudentResponses, service: ResponsesService = Depends(get_student_responses_service)):
    try:
        result = service.create_responses(responses)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get(
    "/responses/{email}",
    response_model=Dict[str, Any],
    responses={
        200: {
            "description": "Responses found",
            "content": {
                "application/json": {
                    "example": {
                        "email": "example@example.com",
                        "responses": [
                            {"question_id": "1", "response": "A"},
                            {"question_id": "2", "response": "B"}
                        ]
                    }
                }
            }
        },
        404: {
            "description": "Responses not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Responses not found"
                    }
                }
            }
        }
    }
)
async def get_responses(email: str, service: ResponsesService = Depends(get_student_responses_service)):
    try:
        responses = service.get_responses_by_token(email)
        if not responses:
            raise HTTPException(status_code=404, detail="Responses not found")
        return responses
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete(
    "/responses/delete-by-email/{email}",
    response_model=Dict[str, Any],
    responses={
        200: {
            "description": "All responses deleted for the student",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Deleted 1 responses for student with email: student@example.com",
                        "deleted_count": 1
                    }
                }
            }
        },
        404: {
            "description": "No responses found for the student",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "No responses found for this email"
                    }
                }
            }
        }
    }
)
async def delete_responses_by_email(email: str, service: ResponsesService = Depends(get_student_responses_service)):
    """
    Delete all responses for a student by their email.
    
    **Path Parameters:**
    - `email`: Student's email address
    
    **Response Example:**
    ```json
    {
        "message": "Deleted 1 responses for student with email: student@example.com",
        "deleted_count": 1
    }
    ```
    """
    result = service.delete_responses_by_email(email)
    if result["deleted_count"] == 0:
        raise HTTPException(status_code=404, detail="No responses found for this email")
    return result
