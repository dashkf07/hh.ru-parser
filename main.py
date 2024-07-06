from parser import parser
from selenium import webdriver
from backend.routers import routers
from fastapi import FastAPI


app = FastAPI()

app.include_router(routers.vacancies_routers)




# async def main():
#     data = await parser.get_html_by_key_words(driver, keys)
#     new_data = await parser.get_more_html_by_key_words(driver, data.get('url'))
#
#
# if __name__ == '__main__':
#     asyncio.run(main())

