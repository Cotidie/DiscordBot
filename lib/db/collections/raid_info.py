from pymongo.collection import Collection

"""
    raid_info 콜렉션의 필드
        * name: (str) 보스명
        * location: (str) 출현 장소
        * weekday: (list) 주중 출현시기
        * weekend: (list) 주말 출현시기
        * reward: (list) 주요 보상 목록
        * icon: (str) 아이콘 이미지 링크
        * map: (list) 출현위치 이미지 링크
        * link: (str) 싴갤러스 링크
"""


class RaidInfo(Collection):
    def __init__(self, db, col):
        super().__init__(db, col)
        self.bosses = None

    def get_raid_bosses(self):
        if self.bosses:
            return self.bosses

        self.bosses = []

        my_query = {}               # 모두 찾기
        my_result = {'name': True}  # 보스명만 가져오기

        results = self.find(my_query, my_result)
        for result in results:
            self.bosses.append(result['name'])

        return self.bosses

    def get_raid_boss(self, boss: str):
        """
        :param boss: (str) 찾고자 하는 보스명
        :return: (dict) 결과 딕셔너리. 없으면 None 반환
        """
        my_query = {'name': boss}

        return self.find_one(my_query)

