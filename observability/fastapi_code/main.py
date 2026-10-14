from fastapi import FastAPI, Depends
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy.orm import Session

from database import get_db
from models import Student

app = FastAPI()

Instrumentator().instrument(app).expose(app)

class StudentCreate(BaseModel):
    name: str
    email: str
    class_: str
    section: str


@app.get("/")
def home():
    return {"message": "Hello World"}


@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}


@app.post("/students")
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
):
    new_student = Student(
        name=student.name,
        email=student.email,
        class_=student.class_,
        section=student.section,
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


@app.get("/students")
def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()

    return students