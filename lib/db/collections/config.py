# 스탠다드
from enum       import Enum
from typing     import Union

# 서드파티
from pymongo.collection import Collection

"""
    서버 부하를 줄이기 위하여 봇 설정값을 하나의 문서로 관리하는 컬렉션
    DB의 설정값을 웹에서 직접 변경하는 경우 renew_config를 실행해야 한다.
"""

class Keys(Enum):
    Token       = 'token'
    Guilds      = 'guilds'
    Thumbnail   = 'thumbnail'
    Color       = 'color'
    Birth       = 'birth'


class Config(Collection):
    config = None

    def __init__(self, db, col):
        super().__init__(db, col)
        self.renew_config()

    def get_config(self, key: Union[Keys, str]):
        """
         key에 해당하는 설정값을 가져온다
        :param key: (str || Keys) 가져올 설정값
        :return: 해당 설정값
        """
        key_str = self.__get_valid_key(key)
        if not key_str:
            raise ValueError(f"key({key}) 값이 유효하지 않습니다.")

        # config 객체 없으면 가져오기
        if not Config.config:
            self.renew_config()

        return Config.config[key_str]

    def set_config(self, key, value):
        """
         설정값을 추가하거나 변경한다.
        :param key: (str || Keys) 해당 설정필드
        :param value: 설정값
        :return: None
        """
        if not Config.config:
            self.renew_config()

        Config.config[key] = value

        # DB에 반영
        self.update_one({'name': 'config'}, {'$set': Config.config})

    def renew_config(self):
        """
        DB에서 설정값을 다시 불러들인다
        :return: None
        """
        my_query = {'name': 'config'}
        my_result = {'_id': False, 'name': False}  # _id, name 필드 빼고 전부

        Config.config = self.find_one(my_query, my_result)

    def __get_valid_key(self, key):
        """
        Keys 객체와 호환이 되는지 확인한다.
        :param key: (str || Keys) 확인할 키 (config 필드명)
        :return: (str) 유효한 키 문자열, 유효하지 않으면 None
        """
        if isinstance(key, Keys):
            key_str = key.value
        elif isinstance(key, str):
            key_str = key
        else:
            return None

        valid_keys = [key.value for key in Keys]
        return key_str if key_str in valid_keys else None

