import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from database.database import async_session
from models.models import Vacancy
import re


find_filter_url = 'https://hh.ru/search/vacancy/advanced?hhtmFrom=main'
find_url = 'https://hh.ru/'


def parse_salary(salary_str):

    if (type(salary_str) == dict):
        return salary_str

    salary_data = {'currency': 'roubles', 'text': salary_str}

    if 'до вычета налогов' in salary_str:
        salary_data['type'] = 'taxes'
    elif 'на руки' in salary_str:
        salary_data['type'] = 'hand'
    else:
        salary_data['type'] = None


    salary_values = re.findall(r'\d+', salary_str)
    salary_values = list(map(lambda x: int(x) * 1000, salary_values))
    if len(salary_values) == 0:
        salary_data['salary'] = [None]
    elif len(salary_values) == 2:
        if 'от' in salary_str:
            salary_data['salary'] = [salary_values[0], 999000]
        elif 'до' in salary_str:
            salary_data['salary'] = [0, salary_values[0]]
    elif len(salary_values) == 4:
        salary_data['salary'] = [salary_values[0], salary_values[3]]


    return salary_data


def parse_experience(exp_str):
    exp_values = re.findall(r'\d+', exp_str)
    if len(exp_values) == 0:
        return [0, 0]
    if exp_values[0] == 6:
        return [6, 100]
    return list(map(int, exp_values))


async def get_html_by_key_words(driver, key_words):

    print('START')
    # переход на страницу
    driver.get('https://hh.ru/')

    # получение элемента input
    inp = driver.find_element(By.NAME, 'text')
    inp.clear()
    inp.send_keys(key_words)

    # получение элемента кнопки "Найти" и нажатие на нее
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[data-qa='search-button']")
    submit_button.click()

    # ожидание загрузки страницы
    wait = WebDriverWait(driver, 500)
    wait.until(EC.visibility_of_element_located((By.ID, "a11y-main-content")))

    soup = BeautifulSoup(driver.page_source, 'lxml')

    # поиск всех карточек вакансий
    vacancies = soup.find_all('div', class_='vacancy-card--z_UXteNo7bRGzxWVcL7y')

    vacancies_data = []

    # итерация по всем карточкам вакансий
    for vacancy in vacancies:
        # получение данных с карточки
        vacancy_name = vacancy.find('span', class_='vacancy-name--c1Lay3KouCl7XasYakLk').get_text().replace('\xa0', ' ').replace('\u202f', ' ')

        vacancy_salary_text = (vacancy.find('div', class_='compensation-labels--uUto71l5gcnhU2I8TZmz')
                          .find('span', 'fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni'))

        print(vacancy_salary_text)
        if (vacancy_salary_text == None):
            vacancy_salary = {'salary': [0, 99999999999999999], 'type': None, 'currency': None, 'text': 'Не указано'}
        else:
            # функция parse_salary используется для обработки текста
            vacancy_salary = parse_salary(vacancy_salary_text.get_text().replace('\xa0', ' ').replace('\u202f', ' '))

        vacancy_experience = vacancy.find('span', class_='label--rWRLMsbliNlu_OMkM_D3').get_text()
        vacancy_company = vacancy.find('span', class_='company-info-text--vgvZouLtf8jwBmaD1xgp').get_text().replace('\xa0', ' ').replace('\u202f', ' ')

        vacancy_city = ((vacancy.find(attrs={"data-qa": "vacancy-serp__vacancy-address"}))
                          .find('span', class_='fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni')).get_text().replace('\xa0', ' ').replace('\u202f', ' ')

        vacancies_data.append({
            'name': vacancy_name,
            'salary': vacancy_salary,
            # функция parse_experience используется для обработки текста опыта в вакансии
            'experience': parse_experience(vacancy_experience),
            'experience_text': vacancy_experience,
            'company': vacancy_company,
            'city': vacancy_city

        })



        vacancy_to_send = {
                'name': vacancy_name,
                'salary': vacancy_salary.get('text'),
                'experience': vacancy_experience,
                'company': vacancy_company,
                'city': vacancy_city

            }

        # добавление вакансии в базу данных
        async with async_session() as session:
            session.add(Vacancy(**vacancy_to_send))
            await session.commit()

    return {
        'vacancies_data': vacancies_data,
        # url возвращается для того, чтобы если пользователь захотел получить еще данные, то при следующем запросе к
        # к серверу эмулятор открылся на странице с данным url и нажал кнопку 'дальше'
        'url': driver.current_url
    }


async def get_more_html_by_key_words(driver, url):
    # эмулятор открывает заданных url
    driver.get(url)

    # ищет кнопку 'дальше' и нажимает на нее
    next_button_element = driver.find_element(By.CSS_SELECTOR, "a[data-qa='pager-next']")
    driver.execute_script("arguments[0].click();", next_button_element)

    # далее все происходит аналогично прошлой функции

    wait = WebDriverWait(driver, 500)
    wait.until(EC.visibility_of_element_located((By.ID, "a11y-main-content")))

    soup = BeautifulSoup(driver.page_source, 'lxml')

    vacancies = soup.find_all('div', class_='vacancy-card--z_UXteNo7bRGzxWVcL7y')

    vacancies_data = []

    # итерация по всем карточкам вакансий
    for vacancy in vacancies:
        # получение данных с карточки
        vacancy_name = vacancy.find('span', class_='vacancy-name--c1Lay3KouCl7XasYakLk').get_text().replace('\xa0',
                                                                                                            ' ').replace(
            '\u202f', ' ')

        vacancy_salary_text = (vacancy.find('div', class_='compensation-labels--uUto71l5gcnhU2I8TZmz')
                               .find('span', 'fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni'))

        print(vacancy_salary_text)
        if (vacancy_salary_text == None):
            vacancy_salary = {'salary': [0, 99999999999999999], 'type': None, 'currency': None, 'text': 'Не указано'}
        else:
            # функция parse_salary используется для обработки текста
            vacancy_salary = parse_salary(vacancy_salary_text.get_text().replace('\xa0', ' ').replace('\u202f', ' '))

        vacancy_experience = vacancy.find('span', class_='label--rWRLMsbliNlu_OMkM_D3').get_text()
        vacancy_company = vacancy.find('span', class_='company-info-text--vgvZouLtf8jwBmaD1xgp').get_text().replace(
            '\xa0', ' ').replace('\u202f', ' ')

        vacancy_city = ((vacancy.find(attrs={"data-qa": "vacancy-serp__vacancy-address"}))
                        .find('span', class_='fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni')).get_text().replace(
            '\xa0', ' ').replace('\u202f', ' ')

        vacancies_data.append({
            'name': vacancy_name,
            'salary': vacancy_salary,
            # функция parse_experience используется для обработки текста опыта в вакансии
            'experience': parse_experience(vacancy_experience),
            'experience_text': vacancy_experience,
            'company': vacancy_company,
            'city': vacancy_city

        })

        vacancy_to_send = {
            'name': vacancy_name,
            'salary': vacancy_salary.get('text'),
            'experience': vacancy_experience,
            'company': vacancy_company,
            'city': vacancy_city

        }

        # добавление вакансии в базу данных
        async with async_session() as session:
            session.add(Vacancy(**vacancy_to_send))
            await session.commit()

    return {
        'vacancies_data': vacancies_data,
        # url возвращается для того, чтобы если пользователь захотел получить еще данные, то при следующем запросе к
        # к серверу эмулятор открылся на странице с данным url и нажал кнопку 'дальше'
        'url': driver.current_url
    }

