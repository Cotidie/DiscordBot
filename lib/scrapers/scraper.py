import bs4.element
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession

class Scraper(BeautifulSoup):
    browser = HTMLSession()

    def __init__(self, url):
        html = self.get_html(url)
        super().__init__(html, 'html.parser')

    def get_html(self, url):
        session = Scraper.browser.get(url)
        session.html.render()

        return session.html.html

    # 부모로부터 몇 번째 자식에 해당하는가를 구한다
    def get_index_from_parent(self, child:bs4.element.Tag):
        """

        :param
            child: 몇 번째 자식인지 알고자 하는 노드
        :return:
            (int) 0으로 시작하는 인덱스
        """

        index = 0

        # 형제들을 순회하며 비교한다
        siblings = child.parent.children
        for tag in siblings:
            if tag == child:
                break
            index += 1

        return index

