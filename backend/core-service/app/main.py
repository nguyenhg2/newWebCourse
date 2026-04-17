from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import auth, courses, sections, lessons, categories
from app.db.database import engine, Base, User, Course, Category, Section as SectionModel, Lesson as LessonModel, get_db

Base.metadata.create_all(bind=engine)

app=FastAPI()

app.add_middleware(CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])

app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(sections.router)
app.include_router(lessons.router)
app.include_router(categories.router)

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)