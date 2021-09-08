from enum   import Enum

from pymongo.collection import Collection


class Keys(Enum):
    Day     = 'day'
    Items   = 'items'
    Alt     = 'alt'
    Effects = 'effects'
    Update  = 'update'


class DayEffect(Collection):
    def __init__(self, db, col_name):
        super().__init__(db, col_name)

    def get_day_info(self, day: int):
        """
        찾고자 하는 요일 정보
        :param day: (int) 월요일이 0
        :return: (dict) 결과 딕셔너리. 없으면 None 반환
        """
        my_query = {Keys.Day.value: day}

        return self.find_one(my_query)