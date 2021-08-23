import sys
import asyncio
from os.path import isfile
import datetime

from glob import glob
import requests
from bs4 import BeautifulSoup


# from lib.scrapers.sigkill import sigkill_scraper
# from lib.db.db     import DB

def file_read():
    if not isfile("db_host.0"):
        print("db_host.0을 찾지 못했습니다.")
    else:
        with open("db_host.0") as file:
            print(file.read())


def check_debug_mode():
    gettrace = getattr(sys, 'gettraace', lambda: None)

    # sys에 gettrace가 없다면 실행 모드
    if gettrace is None:
        print("We are running on Run mode")
    else:
        print("We are on Debug Mode")


def get_db_config():
    token = DB.get_config("TOKEN_BOT")
    print(token)


def get_today_event():
    events = sigkill_scraper.scrape_today_missions()
    print(events)


from selenium import webdriver


def test_selenium():
    driver = webdriver.PhantomJS()
    driver.get("https://mabi.sigkill.kr/todaymission/")

    print(driver.page_source)


def db_set_today_event():
    from lib.db.db import DB

    today = datetime.datetime.now()
    event = "오늘의 미션!"
    DB.insert_today_missions(today, event)

    day = today.date()
    print(type(day))
    event = "오늘의 미션! 날짜 형식"
    DB.insert_today_missions(day, event)


def scraping_test():
    from lib.scrapers.scraper import Scraper
    from lib.scrapers.sigkill import sigkill_scraper

    list = sigkill_scraper.scrape_today_missions()
    print(list)
    sigkill_scraper.browser.quit()

scraping_test()
