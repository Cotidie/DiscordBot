from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# 스크레이퍼, 등록한 이벤트의 주기적 동작을 위한 클래스
class Scheduler(AsyncIOScheduler):
    def __init__(self):
        super().__init__()

