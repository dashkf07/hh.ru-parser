from fastapi import APIRouter
from pydantic import BaseModel
from parser import parser
from selenium import webdriver
from utils.utils import filter_vacancies
from typing import List, Optional


vacancies_routers = APIRouter()


class VacanciesByKeyWordsSchema(BaseModel):
    keywords: str


class FilteredVacanciesSchema(BaseModel):
    min_salary: Optional[int] = None
    max_salary: Optional[int] = None
    min_experience: Optional[int] = None
    max_experience: Optional[int] = None
    company: Optional[str] = None
    city: Optional[str] = None


@vacancies_routers.post('/get_vacancies_by_key_words')
async def get_vacancies_by_key_words(keywords: VacanciesByKeyWordsSchema):
    browser_driver = webdriver.Firefox()
    vacancies = await parser.get_html_by_key_words(driver=browser_driver, key_words='разработчик Java')
    browser_driver.quit()
    return vacancies


@vacancies_routers.post('/get_more_vacancies')
async def get_more_vacancies(url: str):
    browser_driver = webdriver.Firefox()
    vacancies = await parser.get_more_html_by_key_words(driver=browser_driver, url=url)
    return vacancies


@vacancies_routers.post('/get_filtered_vacancies')
async def get_filtered_vacancies(options: FilteredVacanciesSchema):

    user_options = options.model_dump()
    min_salary = user_options.get('min_salary')
    max_salary = user_options.get('max_salary')
    min_experience = user_options.get('min_experience')
    max_experience = user_options.get('max_experience')
    city = user_options.get('city')
    company = user_options.get('company')

    browser_driver = webdriver.Firefox()
    vacancies = await parser.get_html_by_key_words(driver=browser_driver, key_words='разработчик Java')

    filtered = filter_vacancies(vacancies.get('vacancies_data'), min_salary=min_salary, max_salary=max_salary,
                                min_experience=min_experience, max_experience=max_experience, company=company, city=city)
    return filtered


