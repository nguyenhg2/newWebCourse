from pydantic import BaseModel, Field
from typing import Optional
from app.models.common import Level

class CourseBase(BaseModel):
    title: str
    description: str
    thumbnail: Optional[str] = None
    price: float = 0.0
    category_id: int
    level: Level
    rating: float = 0.0

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    thumbnail: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None
    level: Optional[Level] = None
    
class CourseResponse(CourseBase):
    id: int

    class Config:
        from_attributes = True