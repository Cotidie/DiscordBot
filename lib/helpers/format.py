import datetime as dt

"""
    각종 자료형을 이용하기 쉽게 바꾸어주는 클래스
"""


class Formatter:
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