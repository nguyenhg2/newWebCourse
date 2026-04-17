from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import require_role
from app.models.sections import Section, UpdateSection, SectionResponse
from app.db.database import get_db, Section as SectionModel

router=APIRouter()

@router.post("/api/courses/{course_id}/sections", response_model=SectionResponse)
async def create_section(course_id: int, payload: Section, db=Depends(get_db), user=Depends(require_role("admin"))):
    new_section = SectionModel(
        course_id=course_id,
        title=payload.title,
        order=payload.order
    )
    db.add(new_section)
    db.commit()
    db.refresh(new_section)
    return new_section

@router.put("/api/sections/{section_id}", response_model=SectionResponse)
async def update_section(section_id: int, payload: UpdateSection, db=Depends(get_db), user=Depends(require_role("admin"))):
    section = db.query(SectionModel).filter(SectionModel.id == section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Không tìm thấy section")
    section.title = payload.title
    section.order = payload.order
    db.commit()
    db.refresh(section)
    return section

@router.delete("/api/sections/{section_id}")
async def delete_section(section_id: int, db=Depends(get_db), user=Depends(require_role("admin"))):
    section = db.query(SectionModel).filter(SectionModel.id == section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Không tìm thấy section")
    db.delete(section)
    db.commit()
    return {"message": "Section đã được xóa"}