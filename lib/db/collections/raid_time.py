from pymongo.collection import Collection
from datetime           import datetime

"""
    raid_time 컬렉션 필드
    * time: (int) 0~2330까지 시간을 숫자로 표현
    * raid: (str) 레이드 보스 명
    * until: (int) 레이드 종료 시간, 레이드가 없으면 0
    * weekday: (bool) 주중 여부
"""


# 정수형 시간 클래스 (18:30 => 1830)
class IntTime:
    def __init__(self, hour=0, minute=0, time_str: str="", dt: datetime=None):
        self.value = 0

        if time_str != "":
            self.parse_str(time_str)
        elif dt != None:
            self.parse_datetime(dt)
        else:
            self.set_time(hour, minute)


    def get_hour(self):
        return self.value // 100

    def get_minute(self):
        return self.value % 100

    def add_time(self, hour=0, minute=0):
        if hour == 0 and minute == 0:
            return self.value
        # 먼저 분 추가
        added_minute = self.get_minute() + minute
        new_minute = added_minute % 60

        # 시간 추가
        plus_hour = added_minute // 60
        added_hour = self.get_hour() + plus_hour
        new_hour = added_hour % 24

        # 결과 반영
        self.value = new_hour * 100 + new_minute

    def set_time(self, hour=0, minute=0):
        self.value = hour * 100 + minute

    def parse_str(self, time_str: str):
        """
         hh:mm 형식으로 된 문자열을 시간으로 해석한다.
        :param time_str: (str) hh:mm 형식의 문자열
        :return: None, 자신에게 반영한다.
        """
        pass

    def parse_int(self, time_int: int):
        """
         hhmm 형식으로 된 정수를 시간으로 해석한다.
        :param time_int: (int) 0, 130 따위의 정수
        :return: None, 자신에게 반영한다.
        """
        hour = time_int // 100
        minute = time_int % 100

        self.set_time(hour, minute)

    def parse_datetime(self, dt: datetime):
        """
         datetime.datetime 객체를 해석하여 반영한다.
        :param dt: datetime.datetime 객체
        :return: None, 자신에게 반영한다.
        """
        hour = dt.hour
        minute = dt.minute

        self.set_time(hour, minute)

class RaidTime(Collection):
    def __init__(self, db, col_name):
        super().__init__(db, col_name)

    def get_current_raids(self, time):
        pass

    def update_raid_time(self, time: str, raid: str, until: str, weekday: bool):
        pass

    def clear_all(self):
        # 모든 항목의 raid, until을 비운다.
        self.update_many({}, { '$set': {
            'raid': "",
            'until': 0
        }})

        print("raid_time 컬렉션 정리 완료")

