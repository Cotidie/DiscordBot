from abc import *

"""
    자원관리용 클래스
    close(): 자신의 메모리를 해제한다
"""
class IClosable(metaclass=ABCMeta):
    @abstractmethod
    def close(self):
        pass
