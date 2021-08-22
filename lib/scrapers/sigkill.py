from lib.scrapers.scraper import Scraper
from config import CONFIG


class SigKillScraper(Scraper):
    def __init__(self):
        self.url = CONFIG['URL']['SIGKILL']
        super().__init__(self.url)

    def get_today_events(self):
        # 1. class=fc-today, tag=td를 찾는다.
        today_td = self.find("td", class_="fc-today")

        # 2. tr에서 몇 번째 자식인지 구한다.
        index = self.get_index_from_parent(today_td)

        # 3. fc-row 클래스를 가진 div까지 올라간다.
        p_div = today_td.find_parent("div", class_="fc-row")
        table = p_div.find("div", class_="fc-content-skeleton")

        # 4. tbody 자식의 모든 tr을 가져온다.
        tbody = table.find("tbody")
        trs = tbody.find_all("tr")

        # 5. tr 내 fc-title 클래스의 텍스트를 가져온다.
        result = []
        for tr in trs:
            td = list(tr.children)[index]
            text = td.find(class_="fc-title").text
            result.append(text)
        
        # 결과 반환
        return result


sigkill_scraper = SigKillScraper()
