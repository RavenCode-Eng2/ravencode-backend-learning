from typing import List, Optional, Dict, Any
from ...DB.database import ASSESSMENTS_COLLECTION
from ...models.assessments.assessment import Assessment, AssessmentCreate, AssessmentUpdate
from ..base import BaseService

class AssessmentService(BaseService):
    def __init__(self):
        super().__init__(ASSESSMENTS_COLLECTION)
    
    async def create_assessment(self, assessment: AssessmentCreate) -> Assessment:
        """Create a new assessment."""
        # Ensure the order is unique within the module
        if await self.exists({"module_id": assessment.module_id, "order": assessment.order}):
            # If order exists, shift all assessments with >= order up by 1
            collection = await self.get_collection()
            await collection.update_many(
                {
                    "module_id": assessment.module_id,
                    "order": {"$gte": assessment.order}
                },
                {"$inc": {"order": 1}}
            )
        
        assessment_dict = await self.create(assessment)
        return Assessment.model_validate(assessment_dict)
    
    async def get_assessment(self, assessment_id: str) -> Optional[Assessment]:
        """Get an assessment by ID."""
        assessment_dict = await self.get_by_id(assessment_id)
        return Assessment.model_validate(assessment_dict) if assessment_dict else None
    
    async def list_assessments(
        self,
        module_id: str,
        skip: int = 0,
        limit: int = 100,
        include_archived: bool = False
    ) -> List[Assessment]:
        """List assessments for a module."""
        filter_query: Dict[str, Any] = {"module_id": module_id}
        
        if not include_archived:
            filter_query["status"] = {"$ne": "archived"}
            
        assessments = await self.get_all(
            skip=skip,
            limit=limit,
            filter_query=filter_query,
            sort=[("order", 1)]  # Sort by order ascending
        )
        return [Assessment.model_validate(assessment) for assessment in assessments]
    
    async def update_assessment(
        self,
        assessment_id: str,
        assessment_update: AssessmentUpdate
    ) -> Optional[Assessment]:
        """Update an assessment."""
        current_assessment = await self.get_assessment(assessment_id)
        if not current_assessment:
            return None
            
        # If order is being updated, handle reordering
        if assessment_update.order is not None and assessment_update.order != current_assessment.order:
            collection = await self.get_collection()
            if assessment_update.order > current_assessment.order:
                # Moving down: decrease order of assessments in between
                await collection.update_many(
                    {
                        "module_id": current_assessment.module_id,
                        "order": {"$gt": current_assessment.order, "$lte": assessment_update.order}
                    },
                    {"$inc": {"order": -1}}
                )
            else:
                # Moving up: increase order of assessments in between
                await collection.update_many(
                    {
                        "module_id": current_assessment.module_id,
                        "order": {"$gte": assessment_update.order, "$lt": current_assessment.order}
                    },
                    {"$inc": {"order": 1}}
                )
        
        assessment_dict = await self.update(assessment_id, assessment_update)
        return Assessment.model_validate(assessment_dict) if assessment_dict else None
    
    async def delete_assessment(self, assessment_id: str) -> bool:
        """Delete an assessment."""
        current_assessment = await self.get_assessment(assessment_id)
        if not current_assessment:
            return False
            
        # Shift all assessments with higher order down by 1
        collection = await self.get_collection()
        await collection.update_many(
            {
                "module_id": current_assessment.module_id,
                "order": {"$gt": current_assessment.order}
            },
            {"$inc": {"order": -1}}
        )
        
        return await self.delete(assessment_id) 