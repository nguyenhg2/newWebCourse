from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.lessons import Lesson, UpdateLesson, LessonResponse
from app.db.database import get_db, Lesson as LessonModel
from app.core.deps import require_role

router=APIRouter()

@router.post("/api/sections/{section_id}/lessons", response_model=LessonResponse)
async def create_lesson(section_id: int, lesson: Lesson, db=Depends(get_db), user=Depends(require_role("admin"))):
    lesson_data = LessonModel(
        section_id=section_id,
        course_id=lesson.course_id,
        title=lesson.title,
        video_url=lesson.video_url,
        duration=lesson.duration,
        is_free_preview=lesson.is_free_preview
    )
    db.add(lesson_data)
    db.commit()
    db.refresh(lesson_data)
    return lesson_data

@router.put("/api/lessons/{lesson_id}", response_model=LessonResponse)
async def update_lesson(lesson_id: int, lesson: UpdateLesson, db=Depends(get_db), user=Depends(require_role("admin"))):
    lesson_data = db.query(LessonModel).filter(LessonModel.id == lesson_id).first()
    if not lesson_data:
        return {"error": "Lesson not found or no changes made"}
    
    update_dict = lesson.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(lesson_data, key, value)
    
    db.commit()
    db.refresh(lesson_data)
    return lesson_data

@router.delete("/api/lessons/{lesson_id}")
async def delete_lesson(lesson_id: int, db=Depends(get_db), user=Depends(require_role("admin"))):
    lesson_data = db.query(LessonModel).filter(LessonModel.id == lesson_id).first()
    if not lesson_data:
        return {"error": "Không tìm thấy lesson"}
    db.delete(lesson_data)
    db.commit()
    return {"message": "Đã xóa thành công lesson"}
