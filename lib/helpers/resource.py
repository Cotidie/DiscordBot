from lib.interfaces import IClosable

"""
    데몬 프로세스 및 메모리 관리
    여기에 등록될 객체는 반드시 IClosable를 상속받아야 한다
"""


# 싱글톤 클래스
class ResourceManager:
    __instance = None

    def __init__(self):
        if ResourceManager.__instance is not None:
            raise Exception("자원관리자는 싱글톤 객체입니다.")

        self.objects = []
        ResourceManager.__instance = self

    @staticmethod
    def instance():
        if ResourceManager.__instance is None:
            ResourceManager.__instance = ResourceManager()

        return ResourceManager.__instance

    # 객체 추가
    def add(self, obj: IClosable):
        if not isinstance(obj, IClosable):
            raise TypeError(str(type(obj)) + "는 IClosable이 아닙니다.")

        self.objects.append(obj)

    # 모든 객체를 해제
    def close_all(self):
        for obj in self.objects:
            obj.close()
