from sqlalchemy import MetaData, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Vacancy(Base):
    __tablename__ = 'Vacancy'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    company: Mapped[str]
    salary: Mapped[str]
    city: Mapped[str]
    experience: Mapped[str]

