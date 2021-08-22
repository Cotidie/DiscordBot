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
    print(r.html.html)

request = requests.get('https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find')
html = request.text

bs = BeautifulSoup(html, 'html.parser')
print(type(bs.find("div")))