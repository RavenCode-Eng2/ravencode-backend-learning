from typing import Optional, Dict, Any, List
from datetime import datetime
from ...DB.database import PROGRESS_COLLECTION
from ...models.progress.progress import (
    CourseProgress,
    ModuleProgress,
    ContentProgress,
    ProgressStatus,
    ContentType
)
from ..base import BaseService

class ProgressService(BaseService):
    def __init__(self):
        super().__init__(PROGRESS_COLLECTION)

    async def get_course_progress(
        self,
        user_id: str,
        course_id: str
    ) -> Optional[CourseProgress]:
        """Get a user's progress in a course."""
        progress_dict = await self.get_one({"user_id": user_id, "course_id": course_id})
        return CourseProgress.model_validate(progress_dict) if progress_dict else None

    async def list_user_progress(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[CourseProgress]:
        """List all courses progress for a user."""
        progress_list = await self.get_all(
            skip=skip,
            limit=limit,
            filter_query={"user_id": user_id}
        )
        return [CourseProgress.model_validate(p) for p in progress_list]

    async def initialize_course_progress(
        self,
        user_id: str,
        course_id: str
    ) -> CourseProgress:
        """Initialize progress tracking for a course."""
        # Check if progress already exists
        existing = await self.get_course_progress(user_id, course_id)
        if existing:
            return existing

        # Create new progress
        progress = CourseProgress(
            user_id=user_id,
            course_id=course_id,
            started_at=datetime.utcnow()
        )
        progress_dict = await self.create(progress)
        return CourseProgress.model_validate(progress_dict)

    async def update_content_progress(
        self,
        user_id: str,
        course_id: str,
        module_id: str,
        content_id: str,
        content_type: ContentType,
        time_spent: int,
        last_position: Optional[Dict[str, Any]] = None,
        completed: bool = False
    ) -> Optional[CourseProgress]:
        """Update progress for a specific content item (lesson or assessment)."""
        # Get or create course progress
        progress = await self.get_course_progress(user_id, course_id)
        if not progress:
            progress = await self.initialize_course_progress(user_id, course_id)

        # Initialize module progress if needed
        if module_id not in progress.module_progress:
            progress.module_progress[module_id] = ModuleProgress(
                module_id=module_id,
                started_at=datetime.utcnow()
            )

        module_prog = progress.module_progress[module_id]
        
        # Initialize or update content progress
        if content_id not in module_prog.content_progress:
            content_prog = ContentProgress(
                status=ProgressStatus.IN_PROGRESS,
                started_at=datetime.utcnow(),
                time_spent_seconds=time_spent,
                last_position=last_position
            )
        else:
            content_prog = module_prog.content_progress[content_id]
            content_prog.time_spent_seconds += time_spent
            content_prog.last_position = last_position
            content_prog.status = ProgressStatus.COMPLETED if completed else ProgressStatus.IN_PROGRESS

        if completed and not content_prog.completed_at:
            content_prog.completed_at = datetime.utcnow()

        module_prog.content_progress[content_id] = content_prog

        # Update module status
        all_completed = all(
            p.status == ProgressStatus.COMPLETED
            for p in module_prog.content_progress.values()
        )
        if all_completed:
            module_prog.status = ProgressStatus.COMPLETED
            module_prog.completed_at = datetime.utcnow()
        else:
            module_prog.status = ProgressStatus.IN_PROGRESS

        # Update course status
        all_modules_completed = all(
            m.status == ProgressStatus.COMPLETED
            for m in progress.module_progress.values()
        )
        if all_modules_completed:
            progress.status = ProgressStatus.COMPLETED
            progress.completed_at = datetime.utcnow()
        else:
            progress.status = ProgressStatus.IN_PROGRESS

        # Update last accessed time
        progress.last_accessed_at = datetime.utcnow()

        # Save changes
        updated_dict = await self.update(
            progress.id,
            progress.model_dump(exclude={"id"})
        )
        return CourseProgress.model_validate(updated_dict) if updated_dict else None 