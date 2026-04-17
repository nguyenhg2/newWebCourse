from enum import Enum

class Role(str, Enum):
    student = "student"
    admin = "admin"

class Level(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"
