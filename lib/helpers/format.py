import datetime as dt
import pytz

"""
    각종 자료형을 이용하기 쉽게 바꾸어주는 클래스
"""


class Formatter:
    weekdays = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']

    @staticmethod
    def get_day_string(day: int):
        """
        요일 숫자를 한글 요일명으로 반환한다.
        :param day: (int) 월요일을 0으로 하는 정수
        :return: (str) 한글 요일명
        """
        return Formatter.weekdays[day]

    @staticmethod
    def get_date_string(date):
        """
        datetime.datetime 또는 datetime.date를 문자열로 변환한다.
        :param date: (datetime.datetime) || (datetime.date)
        :return: (str) 2021-08-22 형식의 문자열
        """
        # datetime이 아니면 date 객체
        if not isinstance(date, dt.datetime):
            return str(date)
        else:
            return str(date.date())

    @staticmethod
    def missions_to_list(missions: list):
        """
        오늘의미션 쿼리 탐색 결과를 문자열로 가공한다.
        :param missions: MongoDB find로부터 얻은 결과
        :return: (list) 오늘의 미션 정보
        """
        result = []
        for mission in missions:
            result.append(mission['event'])

        return result

    @staticmethod
    def make_unordered_list(msgs: list, shape):
        """
        리스트에 담긴 문자열들을 순서 없는 목록 형식으로 가공한다.
        :param msgs: (list) 목록 문자열을 만들 리스트
        :param shape: (char or str) 매 줄 앞에 표시할 문자
        :return: (str) 가공된 문자열
        """
        starred = list(map(lambda x: f"{shape} " + x, msgs))
        return '\n'.join(starred)

    @staticmethod
    def get_korean_time(type_name: str):
        """
        시간대에 관계없이 한국 시간을 반환한다.
        :param type_name: datetime 또는 date
        :return: datetime.datetime || datetime.date
        """
        ltype = type_name.lower()
        if ltype not in ['datetime', 'date']:
            raise ValueError("type 인자는 datetime, date 중 하나여야 합니다.")

        kst = pytz.timezone('Asia/Seoul')
        k_now = dt.datetime.now(kst)
        if ltype == 'datetime':
            return k_now
        elif ltype == 'date':
            return k_now.date()

    @staticmethod
    def advanced_item_string(item: dict):
        """
        어드밴스드 아이템 정보를 받아 한줄의 문자열로 만든다
        :param item: (dict) 어드밴드스 아이템
        :return: (str) 한줄 문자열
        """
        name = item['name']
        number = f"{item['num']}개"
        attrs = [number] + item['attr']

        return f'{name}({", ".join(attrs)})'


