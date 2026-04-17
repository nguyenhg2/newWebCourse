from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.categories import Categories, CategoryResponse
from app.core.deps import require_role
from app.db.database import get_db, Category

router=APIRouter()

@router.get("/api/categories", response_model=list[CategoryResponse])
async def categories(db: Session = Depends(get_db)):
    category_list = db.query(Category).all()
    return category_list

@router.post("/api/categories", response_model=CategoryResponse)
async def create_category(payload: Categories, db: Session = Depends(get_db), user=Depends(require_role("admin"))):
    existing = db.query(Category).filter(Category.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Danh mục này đã tồn tại")
    category_doc = Category(
        name=payload.name,
        icon=payload.icon or None
    )
    db.add(category_doc)
    db.commit()
    db.refresh(category_doc)
    return category_doc

@router.put("/api/categories/{category_id}", response_model=CategoryResponse)
async def update_category(category_id: int, payload: Categories, db: Session = Depends(get_db), user=Depends(require_role("admin"))):
    existing = db.query(Category).filter(Category.id == category_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Danh mục không tồn tại")

    update_data = payload.model_dump(exclude_unset=True)
    update_data["icon"] = update_data.get("icon") or None

    for key, value in update_data.items():
        setattr(existing, key, value)

    db.commit()
    db.refresh(existing)
    return existing

@router.delete("/api/categories/{category_id}")
async def delete_category(category_id: int, db: Session = Depends(get_db), user=Depends(require_role("admin"))):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Danh mục không tồn tại")
    db.delete(category)
    db.commit()
    return {"message": "Danh mục đã được xóa"}