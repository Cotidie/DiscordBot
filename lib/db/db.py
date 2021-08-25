# 스탠다드
from enum   import Enum

# 서드파티
from pymongo import MongoClient, errors, collection
from apscheduler.triggers.cron import CronTrigger

# 커스텀
from config             import CONFIG
from lib.db.collections import *
from lib.helpers import Formatter

"""
    * 차후 이벤트, 정보 등으로 분리할 필요 있음.
"""

DEFAULT_HOST = CONFIG['DB']['DEFAULT_HOST']
DEFAULT_DB = CONFIG['DB']['DEFAULT_DB']
COLLECTIONS = CONFIG['DB']['COLLECTIONS']


class DataBase(MongoClient):
    """MongoDB 설정해주는 클래스
    Args:
            host (str, optional): DB 호스트 명. Defaults to None.
            db (str, optional): DB 이름. Defaults to DEFAULT_DB.
            collection (str, optional): Collection 이름. Defaults to DEFAULT_COL
    """
    def __init__(self, host=DEFAULT_HOST, db=DEFAULT_DB):
        super().__init__(host)

        self.db = self[db]
        self.cols = {
            COLLECTIONS['EVENT_TODAY']: EventToday(self.db, COLLECTIONS['EVENT_TODAY']),
            COLLECTIONS['RAID_INFO']: RaidInfo(self.db, COLLECTIONS['RAID_INFO']),
            COLLECTIONS['RAID_TIME']: RaidTime(self.db, COLLECTIONS['RAID_TIME'])
        }
        self.host = host         # DB 호스트 명

    def get_collection(self, name) -> collection.Collection:
        """데이터베이스에서 원하는 pymongo collection을 가져온다
        Args:
                name (str): COLLECTIONS 배열안에 정의된 이름만 가능
        Raises:
                pymongo.erros.CollectionInvalid: 잘못된 Collection 이름
        """
        name = name.upper()

        # Wrapper 클래스가 있으면 Wrapper로 반환
        if name in self.cols:
            return self.cols[name]

        if name not in COLLECTIONS:
            print("콜렉션 이름이 잘못되었으므로 확인해주세요")
            print("콜렉션 이름은 config.py안의 COLLECTIONS에 저장되어 있습니다")
            raise errors.CollectionInvalid("콜렉션{" + name + "} 이름이 잘못되었습니다")

        # 기본 콜렉션 객체
        return self.db[COLLECTIONS[name]]

    def get_config(self, name):
        """DB에 저장된 환경값을 불러온다.
        Args:
            name (str): 환경설정 변수명
        Raises:
            pymongo.erros.InvalidDocument: 잘못된 환경변수 이름
        """
        collection = self.get_collection(COLLECTIONS['CONFIG'])

        my_query    = {'variable': name}            # 검색필드
        my_result   = {'value': True}               # 결과필드

        res = collection.find_one(my_query, my_result)

        if res is None:
            raise errors.InvalidDocument(f"환경설정({name})이 존재하지 않습니다.")

        return res['value']

    # 운영/테스트 용 토큰을 구분하여 가져온다.
    def get_token(self, test=False):
        if test:
            return self.get_config("TOKEN_TEST")
        else:
            return self.get_config("TOKEN_BOT")

    def get_today_missions(self, date):
        """
        오늘의 미션 정보를 가져온다.
        :param date: (datetime.date) 조회할 날짜
        :return: (list) 미션 정보, 없으면 None 반환
        """
        collection = self.get_collection(COLLECTIONS['EVENT_TODAY'])

        date_str = Formatter.get_date_string(date)

        my_query = { 'date': date_str }

        docs = list(collection.find(my_query))
        if len(docs) == 0:
            return None

        # 이벤트를 리스트로 변환한다.
        return Formatter.missions_to_list(docs)

    def insert_today_missions(self, date, event):
        """
        오늘의 미션 정보를 저장한다.
        :param date: (datetime.date || datetime) 등록할 날짜
        :param event: (str) 이벤트 명
        :param cat: (Category)
        :return: None
        """
        collection = self.get_collection(COLLECTIONS['EVENT_TODAY'])

        # 날짜를 문자열로 변환
        date_str = Formatter.get_date_string(date)

        data = {
            'date': date_str,
            'event': event,
        }

        try:
            collection.insert_one(data)
        except Exception as e:
            print("저장에 실패했습니다.")
            print(e)

    def get_raid_bosses(self):
        """
        :return: (list) 레이드 보스 리스트
        """
        return self.cols[COLLECTIONS['RAID_INFO']].get_raid_bosses()

    def get_raid_boss(self, boss):
        """
        :param boss: (str) 찾고자 하는 보스명
        :return: (dict) DB에 있는 보스 정보 반환
        """
        return self.cols[COLLECTIONS['RAID_INFO']].get_raid_boss(boss)

DB = DataBase()