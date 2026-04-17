from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.common import Level
from app.core.deps import require_role
from app.db.database import get_db, Course, Category
from app.models.courses import CourseCreate, CourseResponse
from typing import List, Optional

router = APIRouter()

@router.get("/api/courses", response_model=List[CourseResponse])
async def get_courses(category_id: Optional[int] = None, level: Optional[Level] = None, db: Session = Depends(get_db)):
    query = db.query(Course)
    if category_id:
        query = query.filter(Course.category_id == category_id)
    if level:
        query = query.filter(Course.level == level)
    courses = query.all()
    return courses

@router.get("/api/courses/{course_id}", response_model=CourseResponse)
async def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy khóa học")
    return course

@router.post("/api/courses", response_model=CourseResponse)
async def create_course(payload: CourseCreate, db: Session = Depends(get_db), user=Depends(require_role("admin"))):
    new_course = Course(
        title=payload.title,
        description=payload.description,
        thumbnail=payload.thumbnail,
        price=payload.price,
        category_id=payload.category_id,
        level=payload.level,
        rating=payload.rating
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

@router.put("/api/courses/{course_id}", response_model=CourseResponse)
async def update_course(course_id: int, payload: CourseCreate, db: Session = Depends(get_db), user=Depends(require_role("admin"))):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy khóa học")
    
    update_data = payload.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="Không có dữ liệu nào được cung cấp để cập nhật")
    
    for key, value in update_data.items():
        setattr(course, key, value)
    
    db.commit()
    db.refresh(course)
    return course

@router.delete("/api/courses/{course_id}")
async def delete_course(course_id: int, db: Session = Depends(get_db), user=Depends(require_role("admin"))):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy khóa học")
    db.delete(course)
    db.commit()
    return {"detail": "Khóa học đã được xóa"}