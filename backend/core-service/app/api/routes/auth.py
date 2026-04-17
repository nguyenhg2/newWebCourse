from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.users import LoginRequest, RegisterRequest, TokenResponse, UserUpdate, UserResponse
from app.core.security import create_access_token, get_password_hash, verify_password
from app.db.database import get_db, User
from datetime import timedelta
from app.core.config import settings
from app.core.deps import get_current_user

router=APIRouter()

@router.post("/api/auth/register")
async def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    user_email=payload.email
    existing_user = db.query(User).filter(User.email == user_email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email đã được đăng ký")
    hashed_pwd=get_password_hash(payload.password)
    user_doc=User(
        name=payload.name,
        email=user_email,
        hashed_password=hashed_pwd,
        role="student",
        avatar=payload.avatar or None
    )
    db.add(user_doc)
    db.commit()
    return {"message": "Đăng ký thành công"}

@router.post("/api/auth/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user=db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Email hoặc mật khẩu không đúng")
    if not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Email hoặc mật khẩu không đúng")
    
    token=create_access_token(
        {
            "user_id": user.id,
            "email": user.email,
            "role": user.role.value if hasattr(user.role, 'value') else user.role
        },
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
    )
    return TokenResponse(access_token=token, expires_in=settings.access_token_expire_minutes * 60)

@router.get("/api/auth/me", response_model=UserResponse)
async def get_current_user_endpoint(current_user=Depends(get_current_user)):
    return current_user

@router.put("/api/auth/me", response_model=UserResponse)
async def update_current_user(payload: UserUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    update_data = payload.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    user = db.query(User).filter(User.id == current_user["id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")
    for key, value in update_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    updated_user = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role.value if hasattr(user.role, 'value') else user.role,
        "avatar": user.avatar
    }
    return updated_user