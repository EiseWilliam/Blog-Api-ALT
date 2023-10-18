from pydantic import BaseModel
from bson import ObjectId

class CusObjectId(BaseModel):
    oid: str

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, ObjectId):
            raise ValueError('ObjectId expected')
        return str(v)