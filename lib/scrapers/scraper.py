import bs4.element
import requests
from selenium import webdriver


class Scraper:
    browser = webdriver.PhantomJS()  # 하나만 존재해야 한다.

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
