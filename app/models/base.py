from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, Field, field_validator
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler
    ) -> JsonSchemaValue:
        return {"type": "string"}

class BaseDBModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "json_encoders": {ObjectId: str},
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
    }

class TimestampModel(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class StatusModel(BaseModel):
    is_active: bool = True
    is_deleted: bool = False 