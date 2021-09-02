import os

import bs4.element
import requests
from selenium                           import webdriver
from selenium.webdriver.chrome.options  import Options

from lib.helpers.resource   import ResourceManager
from lib.interfaces         import IClosable


class Scraper:
    browser = None  # 공용 브라우저

    def __init__(self):
        pass

    def get_html(self, url, dynamic: bool = True):
        """
        :param url: (str) 파싱할 URL
        :param dynamic: (bool) 동적 페이지 여부
        :return: (str) html 원본 문자열 정보
        """

        if dynamic:
            Scraper.browser.get(url)
            html = Scraper.browser.page_source
        else:
            response = requests.get(url)
            html = response.text

        return html

    # 부모로부터 몇 번째 자식에 해당하는가를 구한다
    def get_index_from_parent(self, child: bs4.element.Tag):
        """
        :param child: 몇 번째 자식인지 알고자 하는 노드
        :return: (int) 0으로 시작하는 인덱스
        """

        index = 0

        # 형제들을 순회하며 비교한다
        siblings = child.parent.children
        for tag in siblings:
            if tag == child:
                break
            index += 1

        return index


class Browser(webdriver.Chrome, IClosable):
    def __init__(self):
        # 브라우저 옵션 세팅
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--headless')

        # Heroku 환경과 구분하여 초기화
        chrome_bin = os.environ.get("GOOGLE_CHROME_BIN")
        if chrome_bin:
            chrome_options.binary_location = chrome_bin
            super().__init__(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
        else:
            super().__init__(options=chrome_options)

    def close(self):
        self.quit()


# 브라우저 생성 및 자원관리자에 추가
Scraper.browser = Browser()
ResourceManager.instance().add(Scraper.browser)