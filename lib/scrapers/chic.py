from bs4 import BeautifulSoup, Tag
from datetime   import datetime

from config                 import CONFIG
from lib.scrapers.scraper   import Scraper
from lib.db                 import DB


class ChicScraper(Scraper):
    url_raid_timetime = CONFIG['URL']['CHIC']['RAID_TIME']

    def __init__(self):
        super().__init__()

    def syncronize_raid_time(self):
        """
        싴갤러스 레이드 시간표와 DB를 동기화
        :return: True, 동기화 실패 시 False
        """
        html = self.get_html(ChicScraper.url_raid_timetime, dynamic=True)
        parser = BeautifulSoup(html, 'html.parser')
        now = datetime.now()

        # 1. centertable 클래스를 찾는다
        table = parser.find(class_="centertable")

        # 2. 'tbody' 내 모든 td를 순회한다.
        tds = table.select("tbody td")

        # 3. 보스와 시간대 추출
        bosses = DB.get_raid_bosses()
        for td in tds:
            raid_name = self.__get_raid_name(td, bosses)
            start_time, end_time = self.__get_raid_time(td)
            if raid_name == "":
                continue

            # 4. DB에 반영한다
            DB.syncronize_raid_time(raid_name, start_time, end_time, now.weekday() <= 4)

        print("동기화 작업이 완료되었습니다.")

    def __get_raid_name(self, td: Tag, bosses: list):
        # td로부터 보스명 가져오기. 유효하지 않으면 빈 문자열 반환
        node = td.find(class_="raid_name")
        if not node:
            return ""
        if node.text not in bosses:
            return ""

        return node.text

    def __get_raid_time(self, td: Tag):
        # td로부터 레이드 시간을 찾아 시작, 끝으로 분리하여 반환
        node = td.find(class_="raid_time_detail")
        if not node:
            return "", ""

        times = node.text.split("-")

        return times[0], times[1]


chic_scraper = ChicScraper()
