# 스탠다드
from typing import Union

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
# DB 설정
DEFAULT_HOST = CONFIG['DB']['DEFAULT_HOST']
DEFAULT_DB = CONFIG['DB']['DEFAULT_DB']
COLLECTIONS = CONFIG['DB']['COLLECTIONS']
# 컬렉션 명
CONFIG      = COLLECTIONS['CONFIG']
EVENT_TODAY = COLLECTIONS['EVENT_TODAY']
RAID_INFO   = COLLECTIONS['RAID_INFO']
RAID_TIME   = COLLECTIONS['RAID_TIME']


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
            CONFIG: Config(self.db, CONFIG),
            EVENT_TODAY: EventToday(self.db, EVENT_TODAY),
            RAID_INFO: RaidInfo(self.db, RAID_INFO),
            RAID_TIME: RaidTime(self.db, RAID_TIME)
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

    def get_config(self, name: Union[ConfKeys, str]):
        """DB에 저장된 환경값을 불러온다.
        Args:
            name (str): 환경설정 변수명
        Raises:
            pymongo.erros.InvalidDocument: 잘못된 환경변수 이름
        """
        return self.cols[CONFIG].get_config(name)

    def set_config(self, name, value):
        """
         config 컬렉션에 환경설정값을 추가하거나 변경한다.
        :param name: 환경설정 이름
        :param value: 환경설정값
        :return: None
        """
        self.cols[CONFIG].set_config(name, value)

    # 운영/테스트 용 토큰을 구분하여 가져온다.
    def get_token(self, test=False):
        tokens = self.get_config(ConfKeys.Token)
        return tokens['test'] if test else tokens['main']

    def get_today_missions(self, date):
        """
        오늘의 미션 정보를 가져온다.
        :param date: (datetime.date) 조회할 날짜
        :return: (list) 미션 정보, 없으면 None 반환
        """
        collection = self.get_collection(EVENT_TODAY)

        date_str = Formatter.get_date_string(date)

        my_query = { 'date': date_str }

        doc = collection.find_one(my_query)
        if not doc:
            return None

        # 이벤트를 리스트로 변환한다.
        return doc['missions']

    def insert_today_missions(self, date, missions: list):
        """
        오늘의 미션 정보를 저장한다.
        :param date: (datetime.date || datetime) 등록할 날짜
        :param missions: (list) 스크레이핑한 미션 목록
        :return: None
        """
        collection = self.get_collection(EVENT_TODAY)

        # 날짜를 문자열로 변환
        date_str = Formatter.get_date_string(date)

        data = {
            'date': date_str,
            'missions': missions,
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
        return self.cols[RAID_INFO].get_raid_bosses()

    def get_raid_boss(self, boss):
        """
        :param boss: (str) 찾고자 하는 보스명
        :return: (dict) DB에 있는 보스 정보 반환
        """
        return self.cols[RAID_INFO].get_raid_boss(boss)

    def get_current_raids(self, time):
        """
         현재 진행중인 레이드 보스 목록을 반환
        :param time: (datetime.datetime) 현재 날짜와 시간
        :return: (list) 레이드 보스명 리스트
        """
        return self.cols[RAID_TIME].get_current_raids(time)

    def syncronize_raid_time(self, boss: str, start_time: str, end_time: str, weekday: bool):
        """
        DB의 시간표를 해당 보스 정보로 채웁니다.
        :param boss: (str) 레이드 보스명
        :param start_time: (str) hh:mm 형식의 시작 시간
        :param end_time: (str) hh:mm 형식의 끝 시간
        :param weekday: (bool) 주중 여부
        :return: None
        """
        self.cols[RAID_TIME].syncronize_raid_time(boss, start_time, end_time, weekday)


DB = DataBase()