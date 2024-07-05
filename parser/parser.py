import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


find_filter_url = 'https://hh.ru/search/vacancy/advanced?hhtmFrom=main'
find_url = 'https://hh.ru/'




async def get_html_by_key_words(driver, key_words):

    # page
    driver.get(find_url)

    # get input element
    inp = driver.find_element(By.NAME, 'text')
    inp.clear()
    inp.send_keys(key_words)

    # get submit button element
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[data-qa='search-button']")
    submit_button.click()

    wait = WebDriverWait(driver, 500)
    wait.until(EC.visibility_of_element_located((By.ID, "a11y-main-content")))

    soup = BeautifulSoup(driver.page_source, 'lxml')

    vacancies = soup.find_all('div', class_='vacancy-card--z_UXteNo7bRGzxWVcL7y')

    vacancies_data = []
    for vacancy in vacancies:
        vacancy_name = vacancy.find('span', class_='vacancy-name--c1Lay3KouCl7XasYakLk').get_text().replace('\xa0', ' ').replace('\u202f', ' ')
        vacancy_salary = (vacancy.find('div', class_='compensation-labels--uUto71l5gcnhU2I8TZmz')
                          .find('span', 'fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni'))
        if (vacancy_salary == None):
            vacancy_salary = 'Не указано'
        else:
            vacancy_salary = vacancy_salary.get_text().replace('\xa0', ' ').replace('\u202f', ' ')

        vacancy_experience = vacancy.find('span', class_='label--rWRLMsbliNlu_OMkM_D3').get_text()
        vacancy_company = vacancy.find('span', class_='company-info-text--vgvZouLtf8jwBmaD1xgp').get_text().replace('\xa0', ' ').replace('\u202f', ' ')

        vacancy_city = ((vacancy.find(attrs={"data-qa": "vacancy-serp__vacancy-address"}))
                          .find('span', class_='fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni')).get_text().replace('\xa0', ' ').replace('\u202f', ' ')

        vacancies_data.append({
            'name': vacancy_name,
            'salary': vacancy_salary,
            'experience': vacancy_experience,
            'company': vacancy_company,

        })

    return {
        'vacancies_data': vacancies_data,
        'url': driver.current_url
    }


async def get_more_html_by_key_words(driver, url):

    driver.get(url)

    next_button_element = driver.find_element(By.CSS_SELECTOR, "a[data-qa='pager-next']")
    driver.execute_script("arguments[0].click();", next_button_element)


    wait = WebDriverWait(driver, 500)
    wait.until(EC.visibility_of_element_located((By.ID, "a11y-main-content")))

    soup = BeautifulSoup(driver.page_source, 'lxml')

    vacancies = soup.find_all('div', class_='vacancy-card--z_UXteNo7bRGzxWVcL7y')

    vacancies_data = []
    for vacancy in vacancies:
        vacancy_name = vacancy.find('span', class_='vacancy-name--c1Lay3KouCl7XasYakLk').get_text().replace('\xa0', ' ').replace('\u202f', ' ')
        vacancy_salary = (vacancy.find('div', class_='compensation-labels--uUto71l5gcnhU2I8TZmz')
                          .find('span', 'fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni'))
        if (vacancy_salary == None):
            vacancy_salary = 'Не указано'
        else:
            vacancy_salary = vacancy_salary.get_text().replace('\xa0', ' ').replace('\u202f', ' ')

        vacancy_experience = vacancy.find('span', class_='label--rWRLMsbliNlu_OMkM_D3').get_text()
        vacancy_company = vacancy.find('span', class_='company-info-text--vgvZouLtf8jwBmaD1xgp').get_text().replace('\xa0', ' ').replace('\u202f', ' ')

        vacancy_city = ((vacancy.find(attrs={"data-qa": "vacancy-serp__vacancy-address"}))
                          .find('span', class_='fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni')).get_text().replace('\xa0', ' ').replace('\u202f', ' ')

        vacancies_data.append({
            'name': vacancy_name,
            'salary': vacancy_salary,
            'experience': vacancy_experience,
            'company': vacancy_company,

        })

        print({
            'name': vacancy_name,
            'salary': vacancy_salary,
            'experience': vacancy_experience,
            'company': vacancy_company,
            'city': vacancy_city

        })

    return {
        'vacancies_data': vacancies_data,
        'url': driver.current_url
    }




def get_find_html_filter():
    pass
