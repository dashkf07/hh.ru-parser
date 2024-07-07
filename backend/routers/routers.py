from fastapi import APIRouter
from pydantic import BaseModel
from selenium import webdriver
from utils.utils import filter_vacancies
from typing import List, Optional
from parser import parser
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
vacancies_routers = APIRouter()


class VacanciesByKeyWordsSchema(BaseModel):
    keywords: str


class FilteredVacanciesSchema(BaseModel):
    salary_range: Optional[List[int]] = None
    experience_range: Optional[List[int]] = None
    city: Optional[str] = None
    company: Optional[str] = None
    url: Optional[str] = None
    keywords: Optional[str] = None


class UrlScheme(BaseModel):
    url: str


@vacancies_routers.post('/get_vacancies_by_key_words')
async def get_vacancies_by_key_words(keywords: VacanciesByKeyWordsSchema):
    # получим данные которые ввел пользователь
    new_keywords = keywords.model_dump().get('keywords')
    browser_driver = webdriver.Firefox()
    # получим вакансии
    vacancies = await parser.get_html_by_key_words(driver=browser_driver, key_words=new_keywords)
    # выйдем из браузера
    browser_driver.quit()
    return {
        "vacancies_data": vacancies.get('vacancies_data'),
        "url": vacancies.get('url')
    }


@vacancies_routers.post('/get_more_vacancies')
async def get_more_vacancies(url: UrlScheme):
    browser_driver = webdriver.Firefox()
    # получим данные которые ввел пользователь
    new_url = url.model_dump().get('url')
    # получим вакансии
    vacancies = await parser.get_more_html_by_key_words(driver=browser_driver, url=new_url)
    return {
        "vacancies_data": vacancies.get('vacancies_data'),
        "url": vacancies.get('url')
    }


@vacancies_routers.post('/get_filtered_vacancies')
async def get_filtered_vacancies(options: FilteredVacanciesSchema):

    user_options = options.model_dump()
    salary_range = user_options.get('salary_range')
    experience_range = user_options.get('experience_range')
    city = user_options.get('city')
    company = user_options.get('company')
    keywords = user_options.get('keywords')
    url = user_options.get('url')
    browser_driver = webdriver.Firefox()

    vacancies = await parser.get_html_by_key_words(driver=browser_driver, key_words=keywords)
    print('ПОЛУЧЕННЫЕ ВАКАНСИИ')
    filtered = filter_vacancies(vacancies=vacancies.get('vacancies_data'), salary_range=salary_range,
                                experience_range=experience_range, city=city, company=company)
    return {
        "vacancies_data": filtered,
        "url": vacancies.get('url')
    }


@vacancies_routers.post('/get_more_filtered_vacancies')
async def get_more_filtered_vacancies(options: FilteredVacanciesSchema):
    user_options = options.model_dump()
    salary_range = user_options.get('salary_range')
    experience_range = user_options.get('experience_range')
    city = user_options.get('city')
    company = user_options.get('company')
    url = user_options.get('url')
    browser_driver = webdriver.Firefox()

    vacancies = await parser.get_more_html_by_key_words(driver=browser_driver, url=url)
    filtered = filter_vacancies(vacancies=vacancies.get('vacancies_data'), salary_range=salary_range, experience_range=experience_range, city=city, company=company)
    return {
        "vacancies_data": filtered,
        "url": vacancies.get('url')
    }


