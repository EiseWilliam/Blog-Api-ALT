from pydantic import BaseModel


class like(BaseModel):
    item_id: str
    user_id: str
    