from discord.ext.commands import Bot as BotBase
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# 봇이 반응할 접두사
PREFIX = "!"
OWNER_IDS = [525193576716566528]

class Bot(BotBase):
    def __init__(self):
        self.PREFIX     = PREFIX    # 봇이 반응할 접두사
        self.guild      = None      # 속할 서버
        self.ready      = False
        self.scheduler  = AsyncIOScheduler()    # 코드의 주기적 수행

        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS)

    def run(self, version:str):
        self.VERSION = version

        # 토큰 획득
        # Q. 토큰의 역할?
        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("아늑 봇이 정신을 차리고 있습니다...")
        super().run(self.TOKEN, reconnect=True)

    async def on_connect(self):
        print("아늑이가 깨어났습니다!")

    async def on_disconnect(self):
        print("아늑이가 떠났습니다...")

    async def on_ready(self):
        if not self.ready:
            print("아늑이가 준비를 마쳤습니다!")
            self.guild = self.get_guild(878239436381495336)
            self.ready=True
        else:
            print("아늑이가 아직 정신을 못차렸습니다.")
    
    async def on_message(self, message:str):
        # 방어코드
        if not message.match('[0-9]+'):
            print("잘못된 명령어 호출")
            return

        

# 봇 인스턴스 생성
bot = Bot()