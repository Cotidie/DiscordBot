import sys
from os.path import isfile

from glob import glob
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from lib.scrapers.sigkill import sigkill_scraper

def test_dynamic_render():
    url = 'https://mabi.sigkill.kr/todaymission/'
    s = HTMLSession()
    r = s.get(url)
    r.html.render()
    print(type(r.html.html))

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

test_dynamic_render()