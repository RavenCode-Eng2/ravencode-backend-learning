from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from ..models.modules.module import Module, ModuleCreate, ModuleUpdate
from ..models.auth.user import User, UserRole
from ..services.modules.module_service import ModuleService
from ..services.courses.course_service import CourseService
from ..core.auth import get_current_active_user, get_instructor_user

router = APIRouter(prefix="/modules", tags=["modules"])
module_service = ModuleService()
course_service = CourseService()

async def check_course_instructor(
    course_id: str,
    current_user: User
) -> None:
    """Check if user is the course instructor or admin."""
    if current_user.role == UserRole.ADMIN:
        return
        
    course = await course_service.get_course(course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
        
    if str(current_user.id) != course.instructor_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this course's modules"
        )

@router.post("", response_model=Module)
async def create_module(
    module_data: ModuleCreate,
    current_user: Annotated[User, Depends(get_instructor_user)]
) -> Module:
    """Create a new module. Only course instructor or admin can create modules."""
    # Check if user is course instructor
    await check_course_instructor(module_data.course_id, current_user)
    
    # Create module
    module = await module_service.create_module(module_data)
    
    # Add module to course
    await course_service.add_module_to_course(module_data.course_id, str(module.id))
    
    return module

@router.get("", response_model=List[Module])
async def list_modules(
    current_user: Annotated[User, Depends(get_current_active_user)],
    course_id: str,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000),
    include_archived: bool = False
) -> List[Module]:
    """List modules for a course."""
    # Check course access
    course = await course_service.get_course(course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Students can only see modules of published courses
    if (
        current_user.role == UserRole.STUDENT and
        course.status != "published"
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access to unpublished course not allowed"
        )
    
    # Only instructors and admins can see archived modules
    if (
        include_archived and
        current_user.role == UserRole.STUDENT
    ):
        include_archived = False
    
    return await module_service.list_modules(
        course_id=course_id,
        skip=skip,
        limit=limit,
        include_archived=include_archived
    )

@router.get("/{module_id}", response_model=Module)
async def get_module(
    module_id: str,
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> Module:
    """Get a module by ID."""
    module = await module_service.get_module(module_id)
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found"
        )
    
    # Check course access
    course = await course_service.get_course(module.course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Students can only see modules of published courses
    if (
        current_user.role == UserRole.STUDENT and
        course.status != "published"
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access to unpublished course not allowed"
        )
    
    return module

@router.put("/{module_id}", response_model=Module)
async def update_module(
    module_id: str,
    module_update: ModuleUpdate,
    current_user: Annotated[User, Depends(get_instructor_user)]
) -> Module:
    """Update a module. Only course instructor or admin can update."""
    # Get existing module
    module = await module_service.get_module(module_id)
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found"
        )
    
    # Check if user is course instructor
    await check_course_instructor(module.course_id, current_user)
    
    # Update module
    updated_module = await module_service.update_module(module_id, module_update)
    if not updated_module:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update module"
        )
    
    return updated_module

@router.delete("/{module_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_module(
    module_id: str,
    current_user: Annotated[User, Depends(get_instructor_user)]
) -> None:
    """Delete a module. Only course instructor or admin can delete."""
    # Get existing module
    module = await module_service.get_module(module_id)
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found"
        )
    
    # Check if user is course instructor
    await check_course_instructor(module.course_id, current_user)
    
    # Remove module from course
    await course_service.remove_module_from_course(module.course_id, module_id)
    
    # Delete module
    success = await module_service.delete_module(module_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to delete module"
        )

@router.post("/{module_id}/lessons/{lesson_id}", response_model=Module)
async def add_lesson_to_module(
    module_id: str,
    lesson_id: str,
    current_user: Annotated[User, Depends(get_instructor_user)]
) -> Module:
    """Add a lesson to a module. Only course instructor or admin can add lessons."""
    # Get existing module
    module = await module_service.get_module(module_id)
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found"
        )
    
    # Check if user is course instructor
    await check_course_instructor(module.course_id, current_user)
    
    # Add lesson
    updated_module = await module_service.add_lesson_to_module(module_id, lesson_id)
    if not updated_module:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to add lesson to module"
        )
    
    return updated_module

@router.delete("/{module_id}/lessons/{lesson_id}", response_model=Module)
async def remove_lesson_from_module(
    module_id: str,
    lesson_id: str,
    current_user: Annotated[User, Depends(get_instructor_user)]
) -> Module:
    """Remove a lesson from a module. Only course instructor or admin can remove lessons."""
    # Get existing module
    module = await module_service.get_module(module_id)
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found"
        )
    
    # Check if user is course instructor
    await check_course_instructor(module.course_id, current_user)
    
    # Remove lesson
    updated_module = await module_service.remove_lesson_from_module(module_id, lesson_id)
    if not updated_module:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to remove lesson from module"
        )
    
    return updated_module

@router.post("/{module_id}/assessments/{assessment_id}", response_model=Module)
async def add_assessment_to_module(
    module_id: str,
    assessment_id: str,
    current_user: Annotated[User, Depends(get_instructor_user)]
) -> Module:
    """Add an assessment to a module. Only course instructor or admin can add assessments."""
    # Get existing module
    module = await module_service.get_module(module_id)
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found"
        )
    
    # Check if user is course instructor
    await check_course_instructor(module.course_id, current_user)
    
    # Add assessment
    updated_module = await module_service.add_assessment_to_module(module_id, assessment_id)
    if not updated_module:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to add assessment to module"
        )
    
    return updated_module

@router.delete("/{module_id}/assessments/{assessment_id}", response_model=Module)
async def remove_assessment_from_module(
    module_id: str,
    assessment_id: str,
    current_user: Annotated[User, Depends(get_instructor_user)]
) -> Module:
    """Remove an assessment from a module. Only course instructor or admin can remove assessments."""
    # Get existing module
    module = await module_service.get_module(module_id)
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found"
        )
    
    # Check if user is course instructor
    await check_course_instructor(module.course_id, current_user)
    
    # Remove assessment
    updated_module = await module_service.remove_assessment_from_module(module_id, assessment_id)
    if not updated_module:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to remove assessment from module"
        )
    
    return updated_module 