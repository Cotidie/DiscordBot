import sys      # 강제종료
import os       # 환경변수 읽기

from os.path import isfile          # 파일 존재 확인
from datetime import date


"""
    실행 관련 환경설정
    * TEST 환경에서는 lib.bot.__init__에서 전역변수를 TEST로 변경할 것
"""

# MongoDB 주소 얻어오기
if not isfile("db_host.0"):
    HOST = os.environ.get('DB_TOKEN')
    if not HOST:
        sys.exit("DB 토큰을 찾을 수 없습니다. 관리자에게 문의하세요.")
else:
    with open("db_host.0") as file:
        HOST = file.read()

CONFIG = {
    'PREFIX': {
        'MAIN': '!!',
        'TEST': '$$',
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
            'STDOUT': 878239436381495340,     # 일반채팅룸
        },
    },
    'PATH': {
        'COGS': './lib/cogs/',
    },
    'URL': {
        'SIGKILL': 'https://mabi.sigkill.kr/todaymission/',
        'CHIC': {
            'RAID_TIME': 'https://lute.fantazm.net/raid2',
        },
    },
    'DB': {
        'DEFAULT_HOST': HOST,
        'DEFAULT_DB': 'Anuk',
        'COLLECTIONS': {
            'CONFIG': 'config',
            'EVENT_TODAY': 'event_today',
            'RAID_ID': 'raid_id',
            'RAID_INFO': 'raid_info',
            'RAID_TIME': 'raid_time',
        }
    }
}