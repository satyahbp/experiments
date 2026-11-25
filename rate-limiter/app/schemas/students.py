from pydantic import BaseModel

class StudentCreate(BaseModel):
    name: str
    email: str
    class_: str
    section: str