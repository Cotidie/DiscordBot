from bs4 import BeautifulSoup
from datetime   import date

from config                 import CONFIG
from lib.scrapers.scraper   import Scraper
from lib.db.db              import DB

URL_SIGKILL = CONFIG['URL']['SIGKILL']


class SigKillScraper(Scraper):
    def __init__(self):
        super().__init__()

    # 먼저 DB에 존재하는지 확인한다.
    def get_today_missions(self, today: date):
        # DB에 이미 존재하는지 확인한다.
        missions = DB.get_today_missions(today)
        if not missions:
            # 스크레이핑 실행
            missions = self.scrape_today_missions(today)
            if not missions:
                return

            # DB에 저장
            for mission in missions:
                DB.insert_today_missions(today, mission)

        return missions

    def scrape_today_missions(self, today: date):
        html = self.get_html(URL_SIGKILL, dynamic=True)
        parser = BeautifulSoup(html, 'html.parser')

        # 1. 해당 날짜 셀을 찾는다.
        divs = parser.find_all("div", class_="fc-content-skeleton")
        today_td = None
        for div in divs:
            today_td = div.find("td", {'data-date': str(today)})
            if today_td:
                break

        if not today_td:
            return None

        # 2. tr에서 몇 번째 자식인지 구한다.
        index = self.get_index_from_parent(today_td)

        # 3. table까지 올라간다.
        table = today_td.find_parent("table")

        # 4. tbody 자식의 모든 tr을 가져온다.
        trs = table.find("tbody").find_all("tr")

        # 5. tr 내 fc-title 클래스의 텍스트를 가져온다.
        result = []
        for tr in trs:
            td = list(tr.children)[index]
            text = td.find(class_="fc-title").text
            result.append(text)
        
        # 결과 반환
        return result


sigkill_scraper = SigKillScraper()
