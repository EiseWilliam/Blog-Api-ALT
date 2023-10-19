from bson import ObjectId
from pydantic import BaseModel, validator
from typing import Optional, Any

class CusObjectId(BaseModel):
    id: ObjectId

    @classmethod
    def __get_pydantic_field_schema__(cls, model_field):
        return {
            'type': 'string',
            'format': 'objectid',
        }
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(str(v)):
            return ValueError(f"Not a valid ObjectId: {v}")
        return ObjectId(str(v))
    
    class Config:
        arbitrary_types_allowed = True


