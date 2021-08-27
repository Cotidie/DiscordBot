# 스탠다드 라이브러리
import os           # 실행중인 os 종류
from glob           import glob

# 서드파티 라이브러리
import discord
from discord                        import Intents
from discord.ext.commands           import Bot as BotBase
from discord.ext.commands           import CommandNotFound
from discord_slash                  import SlashCommand
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron      import CronTrigger

# 커스텀 모듈
from config         import CONFIG  # 환경설정
from lib.db         import DB
from lib.helpers    import Messenger, Formatter, ResourceManager

"""
    * 리팩토링: ChatManager, ErrorHandler, Handlers > Event, Command
    * 필요기능: 오늘의 이벤트
"""

GUILDS = DB.get_config('guilds')

class Bot(BotBase):
    def __init__(self, test: bool=False):
        # 봇 기본정보
        self.test = test
        self.birth = CONFIG['BOT']['BIRTH']  # 만든 날짜
        self.owners = CONFIG['OWNER_IDS']
        self.prefix = CONFIG['PREFIX']['TEST'] if test else CONFIG['PREFIX']['MAIN']

        # 환경설정
        self.stdout = CONFIG['CHANNEL']['TEST']['STDOUT'] if test else CONFIG['CHANNEL']['MAIN']['STDOUT']
        self.ready = False  # 모든 준비 완료 신호

        self.db = DB                         # MongoDB
        self.scheduler = AsyncIOScheduler()  # 예약 이벤트 수행
        self.token = DB.get_token(test=test)

        # 헬퍼 객체
        self.messenger = Messenger(self)   # 채팅 메시지 생성

        super().__init__(command_prefix=self.prefix,
                         owner_ids=self.owners,
                         intents=Intents.all())

    # 봇 진입점
    def run(self, version: str):
        self.setup()

        print("아늑 봇이 정신을 차리고 있습니다...")
        super().run(self.token, reconnect=True)

    # Cog 불러오기
    def setup(self):
        for cog in Bot.__get_cogs():
            self.load_extension(f"lib.cogs.{cog}")
            print(f" {cog} 코그 로딩 완료")
        print("모든 코그를 로딩했습니다.")

    async def print_message(self):
        await self.stdout.send("1분마다 발송되는 메시지")

    # 디스코드와 연결된 시점
    async def on_connect(self):
        print("아늑이가 깨어났습니다!")

    async def on_disconnect(self):
        print("아늑이가 떠났습니다...")

    # async def on_error(self, err, *args, **kwargs):
    #     # err는 문자열의 에러메시지
    #     if err == "on_command_error":
    #         print(err)
    #         channel = args[0]
    #         await channel.send("Something went wrong")

    async def on_command_error(self, context, exception):
        if isinstance(exception, CommandNotFound):
            print("Wrong Command")
        elif hasattr(exception, "original"):
            raise exception.original
        else:
            raise exception

    async def on_ready(self):
        if not self.ready:
            # 환경설정 세팅
            self.ready = True
            self.stdout = self.get_channel(self.stdout)
            self.scheduler.start()

            # 서버 목록 업데이트
            guilds = [guild.id for guild in self.guilds]
            self.db.set_config('guilds', guilds)

            # ~하는 중 표시
            my_activity = discord.Game("열심히 학습")
            await self.change_presence(activity=my_activity)

            # 인사말 전송
            intro = self.messenger.introduce_self()
            # await self.stdout.send(embed=intro)

            print("아늑이가 준비를 마쳤습니다!")
        else:
            print("아늑이가 아직 정신을 못차렸습니다.")

    # 디스코드의 메시지를 탐지한다.
    async def on_message(self, message: str):
        # 명령어 탐지 및 실행
        await self.process_commands(message)

    @staticmethod
    def __get_cogs():
        cog_path = CONFIG['PATH']['COGS'] + "*.py"

        delimiter = "\\" if os.name == 'nt' else '/'

        # .py cog 파일 가져오기
        filenames = [path.split(delimiter)[-1] for path in glob(cog_path)]
        # .py 제거
        filenames = list(map(lambda f: f[:-3], filenames))
        # __init__ 제거
        filenames.remove("__init__")

        return filenames


# 봇 인스턴스 생성
bot = Bot(test=True)
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)
