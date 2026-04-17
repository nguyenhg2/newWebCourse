from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from app.core.config import settings
import enum

engine = create_engine(
    "mssql+pyodbc:///?odbc_connect=" + settings.sqlserver_connection_string.replace(";", ";"),
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Role(enum.Enum):
    student = "student"
    admin = "admin"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(SQLEnum(Role), default=Role.student)
    avatar = Column(String(500), nullable=True)
    
    courses = relationship("Course", back_populates="author")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    icon = Column(String(500), nullable=True)
    
    courses = relationship("Course", back_populates="category")

class Level(enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(500), nullable=False)
    description = Column(String(2000), nullable=False)
    thumbnail = Column(String(500), nullable=True)
    price = Column(Float, default=0.0)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    level = Column(SQLEnum(Level), nullable=False)
    rating = Column(Float, default=0.0)
    
    category = relationship("Category", back_populates="courses")
    sections = relationship("Section", back_populates="course", cascade="all, delete-orphan")

class Section(Base):
    __tablename__ = "sections"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String(255), nullable=False)
    order = Column(Integer, nullable=False)
    
    course = relationship("Course", back_populates="sections")
    lessons = relationship("Lesson", back_populates="section", cascade="all, delete-orphan")

class Lesson(Base):
    __tablename__ = "lessons"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String(255), nullable=False)
    video_url = Column(String(500), nullable=False)
    duration = Column(Integer, nullable=False)
    is_free_preview = Column(Boolean, default=False)
    
    section = relationship("Section", back_populates="lessons")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()