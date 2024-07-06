from pydantic import BaseModel


class VacanciesByKeyWordsSchema(BaseModel):
    keywords: str


class FilteredVacanciesSchema(BaseModel):
    min_salary: int | None
    max_salary: int | None
    min_experience: int | None
    max_experience: int | None
    company: str | None
    city: str | None
