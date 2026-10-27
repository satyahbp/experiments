from fastapi import FastAPI, Depends, HTTPException, Query
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy.orm import Session

from database import get_db
from models import Student

app = FastAPI(root_path="/api")

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
def get_students(
    sort_by: str = Query(default="id"),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    section: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    allowed_columns = {
        "id": Student.id,
        "name": Student.name,
        "email": Student.email,
        "class_": Student.class_,
        "class": Student.class_,
        "section": Student.section,
    }

    column = allowed_columns.get(sort_by)

    if column is None:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sort_by. Allowed values: {list(allowed_columns.keys())}",
        )

    query = db.query(Student)

    if section is not None:
        query = query.filter(Student.section == section)

    students = (
        query
        .order_by(column, Student.id)
        .limit(limit)
        .offset(offset)
        .all()
    )

    return students