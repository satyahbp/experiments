from sqlalchemy.orm import Session
from fastapi import (
    APIRouter, 
    Depends, 
    Query,
    HTTPException
)

from schemas.students import StudentCreate
from core.database import get_db
from models.student import Student

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


@router.post("/students")
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


@router.get("/students")
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