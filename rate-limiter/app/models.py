from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Student(Base):
    __tablename__ = "student"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(60),
        unique=True,
        nullable=False,
    )

    class_: Mapped[str] = mapped_column(
        "class",
        String(3),
        nullable=False,
    )

    section: Mapped[str] = mapped_column(
        String(1),
        nullable=False,
    )