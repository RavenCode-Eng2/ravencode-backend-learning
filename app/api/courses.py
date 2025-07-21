from typing import Annotated, List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from ..models.courses.course import Course, CourseCreate, CourseUpdate
from ..services.courses.course_service import CourseService

router = APIRouter(prefix="/courses", tags=["courses"])
course_service = CourseService()

@router.post("", response_model=Course)
async def create_course(
    course_data: CourseCreate,
    current_user: Annotated[User, Depends(get_instructor_user)]
) -> Course:
    """Create a new course. Only instructors and admins can create courses."""
    # Set instructor ID
    course_data.instructor_id = str(current_user.id)
    
    # Create course
    course = await course_service.create_course(course_data)
    
    # Add course to instructor's teaching courses
    current_user.teaching_courses.append(str(course.id))
    # TODO: Update user's teaching courses
    
    return course

@router.get("", response_model=List[Course])
async def list_courses(
    current_user: Annotated[User, Depends(get_current_active_user)],
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    instructor_id: Optional[str] = None,
    category: Optional[str] = None,
    level: Optional[str] = None,
    language: Optional[str] = None,
    status: Optional[str] = None,
    search_term: Optional[str] = None
) -> List[Course]:
    """List courses with filtering and search."""
    # If user is not admin or instructor, only show published courses
    if current_user.role == UserRole.STUDENT:
        status = "published"
    
    return await course_service.list_courses(
        skip=skip,
        limit=limit,
        instructor_id=instructor_id,
        category=category,
        level=level,
        language=language,
        status=status,
        search_term=search_term
    )

@router.get("/{course_id}", response_model=Course)
async def get_course(
    course_id: str,
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> Course:
    """Get a course by ID."""
    course = await course_service.get_course(course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Check access permissions
    if current_user.role == UserRole.STUDENT and course.status != "published":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access to unpublished course not allowed"
        )
    
    return course

@router.put("/{course_id}", response_model=Course)
async def update_course(
    course_id: str,
    course_update: CourseUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> Course:
    """Update a course. Only course instructor or admin can update."""
    # Get existing course
    course = await course_service.get_course(course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Check permissions
    if (
        current_user.role != UserRole.ADMIN and
        str(current_user.id) != course.instructor_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this course"
        )
    
    # Update course
    updated_course = await course_service.update_course(course_id, course_update)
    if not updated_course:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update course"
        )
    
    return updated_course

@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(
    course_id: str,
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> None:
    """Delete a course. Only course instructor or admin can delete."""
    # Get existing course
    course = await course_service.get_course(course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Check permissions
    if (
        current_user.role != UserRole.ADMIN and
        str(current_user.id) != course.instructor_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this course"
        )
    
    # Delete course
    success = await course_service.delete_course(course_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to delete course"
        )

@router.post("/{course_id}/modules/{module_id}", response_model=Course)
async def add_module_to_course(
    course_id: str,
    module_id: str,
    current_user: Annotated[User, Depends(get_instructor_user)]
) -> Course:
    """Add a module to a course. Only course instructor or admin can add modules."""
    # Get existing course
    course = await course_service.get_course(course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Check permissions
    if (
        current_user.role != UserRole.ADMIN and
        str(current_user.id) != course.instructor_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this course"
        )
    
    # Add module
    updated_course = await course_service.add_module_to_course(course_id, module_id)
    if not updated_course:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to add module to course"
        )
    
    return updated_course

@router.delete("/{course_id}/modules/{module_id}", response_model=Course)
async def remove_module_from_course(
    course_id: str,
    module_id: str,
    current_user: Annotated[User, Depends(get_instructor_user)]
) -> Course:
    """Remove a module from a course. Only course instructor or admin can remove modules."""
    # Get existing course
    course = await course_service.get_course(course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Check permissions
    if (
        current_user.role != UserRole.ADMIN and
        str(current_user.id) != course.instructor_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this course"
        )
    
    # Remove module
    updated_course = await course_service.remove_module_from_course(course_id, module_id)
    if not updated_course:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to remove module from course"
        )
    
    return updated_course

@router.get("/frontend-data", response_model=List[Dict[str, Any]])
async def get_courses_frontend_data() -> List[Dict[str, Any]]:
    """
    Get all courses with their modules and lessons structured for frontend.
    This endpoint returns data in the format expected by the React frontend.
    """
    return await course_service.get_courses_with_modules_and_lessons() 