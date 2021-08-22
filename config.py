import sys                          # 강제종료

from os.path import isfile          # 파일 존재 확인


"""
    실행 관련 환경설정
"""

# MongoDB 주소 얻어오기
if not isfile("db_host.0"):
    sys.exit("'db_host.0 파일이 없습니다. 관리자에게 문의하세요.")
else:
    with open("db_host.0") as file:
        HOST = file.read()

CONFIG = {
    'PREFIX': "!",
    'GUILD': {
        'MAIN': 488672146990825472,           # 아늑 서버
        'TEST': 878239436381495336,
    },
    'OWNER_IDS': [
        525193576716566528,                   # COTIDIE
        445597833995747329                    # 룬닝
    ],
    'CHANNEL': {
        'MAIN': {
            'STDOUT': 488672146990825474,     # 일반채팅룸
        },
        'TEST': {
            'STDOUT': 878239436381495336,      # 일반채팅룸
        },
    },
    'PATH': {
        'COGS': './lib/cogs/',
    },
    'URL': {
        'SIGKILL': 'https://mabi.sigkill.kr/todaymission/',
        'CHIC': 'https://lute.fantazm.net/today_mission',
    },
    'DB': {
        'DEFAULT_HOST': HOST,
        'DEFAULT_COL': 'event',
        'DEFAULT_DB': 'Discord',
        'COLLECTIONS': {
            'CONFIG': 'config',
            'EVENT': 'event'
        }
    }
}