from typing import Optional
from pydantic import BaseModel

class Categories(BaseModel):
    name: str
    icon: Optional[str] = None

class CategoryResponse(Categories):
    id: int

    class Config:
        from_attributes = True