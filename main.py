from parser import parser
from selenium import webdriver
import asyncio


driver = webdriver.Firefox()
find_url = 'https://hh.ru/'
keys = 'разработчик java'


async def main():
    data = await parser.get_html_by_key_words(driver, keys)
    new_data = await parser.get_more_html_by_key_words(driver, data.get('url'))


if __name__ == '__main__':
    asyncio.run(main())

