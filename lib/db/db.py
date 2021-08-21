from os.path import isfile
from pymongo import MongoClient, errors, collection
from apscheduler.triggers.cron import CronTrigger

DEFAULT_HOST = 'mongodb+srv://admin:1234@links.fc8p4.mongodb.net/PYTHON-LINK-SHORTNER?retryWrites=true&w=majority'
DEFAULT_COL = 'event'
DEFAULT_DB = 'discord_bot_anuk'
COLLECTIONS = {
    'CONFIG': 'config',
    'EVENT': 'event'
}

class DataBase(MongoClient):
    """MongoDB 설정해주는 클래스
    Args:
            host (str, optional): DB 호스트 명. Defaults to None.
            db (str, optional): DB 이름. Defaults to DEFAULT_DB.
            collection (str, optional): Collection 이름. Defaults to DEFAULT_COL
    """
    def __init__(self, host=DEFAULT_HOST, db=DEFAULT_DB, collection=DEFAULT_COL):
        self._db = db                    # DB명
        self._col = collection           # Collection명
        self.host = host         # DB 호스트 명
        super().__init__(self.host)

    def get_collection(self, name='LINKS') -> collection.Collection:
        """데이터베이스에서 원하는 pymongo collection을 가져온다
        Args:
                name (str): COLLECTIONS 배열안에 정의된 이름만 가능
        Raises:
                pymongo.erros.CollectionInvalid: 잘못된 Collection 이름
        """
        name = name.upper()
        if name not in COLLECTIONS:
            print("콜렉션 이름이 잘못되었으므로 확인해주세요")
            print("콜렉션 이름은 mongo_db.py안의 COLLECTIONS에 저장되어 있습니다")
            raise errors.CollectionInvalid("콜렉션{" + name + "} 이름이 잘못되었습니다")

        return self[self._db][COLLECTIONS[name]]

    def get_config(self, name):
        """DB에 저장된 환경값을 불러온다.
        Args:
            name (str): 환경설정 변수명
        Raises:
            pymongo.erros.InvalidDocument: 잘못된 환경변수 이름
        """
        collection = self[self._db][COLLECTIONS['CONFIG']]

        my_query    = {'variable': name}            # 검색필드
        my_result   = {'value': True}               # 결과필드

        res = collection.find_one(my_query, my_result)

        if res is None:
            print(f"변수명 {name}이 존재하지 않습니다.")
            raise errors.InvalidDocument(f"환경설정({name})이 존재하지 않습니다.")

        return res['value']


db = DataBase()