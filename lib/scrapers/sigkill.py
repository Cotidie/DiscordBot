from bs4 import BeautifulSoup
from datetime   import datetime

from config                 import CONFIG
from lib.scrapers.scraper   import Scraper
from lib.db.db              import DB

URL_SIGKILL = CONFIG['URL']['SIGKILL']


class SigKillScraper(Scraper):
    def __init__(self):
        super().__init__()

    # 먼저 DB에 존재하는지 확인한다.
    def get_today_missions(self):
        # DB에 이미 존재하는지 확인한다.
        today = datetime.today().date()
        missions = DB.get_today_missions(today)
        if not missions:
            # 스크레이핑 실행
            missions = self.scrape_today_missions()
            # DB에 저장
            for mission in missions:
                DB.insert_today_missions(today, mission)

        return missions

    def scrape_today_missions(self):
        html = self.get_html(URL_SIGKILL, dynamic=True)
        parser = BeautifulSoup(html, 'html.parser')

        # 1. class=fc-today, tag=td를 찾는다.
        today_td = parser.find("td", class_="fc-today")

        # 2. tr에서 몇 번째 자식인지 구한다.
        index = self.get_index_from_parent(today_td)

        # 3. fc-row 클래스를 가진 div까지 올라간다.
        p_div = today_td.find_parent("div", class_="fc-row")
        table = p_div.find("div", class_="fc-content-skeleton")

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
