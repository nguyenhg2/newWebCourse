from pydantic import BaseModel

class Section(BaseModel):
    course_id: int
    title: str
    order: int

class UpdateSection(BaseModel):
    title: str
    order: int

class SectionResponse(Section):
    id: int

    class Config:
        from_attributes = True