from os.path import isfile
from sqlite3 import connect

# Cron?
from apscheduler.triggers.cron import CronTrigger

DB_PATH = "./data/db/database.db"
BUILD_PATH = "./data/db/build.sql"

# db 연결 및 커서 생성
cxn = connect(DB_PATH, check_same_thread=False)
cur = cxn.cursor()

def with_commit(func):
    def inner(*args, **kwargs):
        func(*args, **kwargs)
        commit()

@with_commit
def build():
    if isfile(BUILD_PATH):
        scriptexec(BUILD_PATH)

# db 커밋
def commit():
    cxn.commit()

# 1분마다 DB와 동기화
def autosave(sched):
    # 1분마다 commit한다
    sched.add_job(commit, CronTrigger(second=0))

# db 종료
def close():
    cxn.close()

def field(command, *values):
    cur.execute(command, tuple(values))

    # fetch 성공 후 값 반환
    if (fetch := cur.fetchone()) is not None:
        return fetch[0]

def record(command, *values):
    cur.execute(command, tuple(values))

    return cur.fetchone()

def records(command, *values):
    cur.execute(command, tuple(values))

    return cur.fetchall()

def column(command, *values):
    cur.execute(command, tuple(values))

    return [list[0] for item in cur.fetchall()]

def execute(command, *values):
    cur.execute(command, tuple(values))

def multiexec(command, valueset):
    cur.executemany(command, valueset)

def scriptexec(path):
    with open(path, "r", encoding="utf-8") as script:
        cur.executescript(script.read())