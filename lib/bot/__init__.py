from datetime import datetime
from glob import glob
from config import CONFIG  # 환경설정
from lib.db.db import db

from discord import Intents, Embed, File
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

"""
    * self.get_server(ID): 속한 서버, 하드코딩됨
    * self.get_channel(ID): 속한 채널, 하드코딩됨
    * 리팩토링: ChatManager, ErrorHandler, Handlers > Event, Command
    * 필요기능: 오늘의 이벤트, 
"""


class Bot(BotBase):
    def __init__(self):
        self.token = Bot.__get_token()
        self.guild = None  # 속할 서버
        self.ready = False

        self.db = db                         # MongoDB
        self.scheduler = AsyncIOScheduler()  # 예약 이벤트 수행

        super().__init__(command_prefix=CONFIG['PREFIX'],
                         owner_ids=CONFIG['OWNER_IDS'],
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
            print(f" {cog} cog loaded")
        print("Setup Completed")

    @staticmethod
    def __get_cogs():
        cog_path = CONFIG['PATH']['COGS'] + "*.py"

        # .py cog 파일 가져오기
        filenames = [path.split("\\")[-1] for path in glob(cog_path)]
        # .py 제거
        filenames = list(map(lambda f: f[:-3], filenames))
        # CogBase 제거
        filenames.remove("CogBase")
        # __init__ 제거
        filenames.remove("__init__")

        return filenames

    @staticmethod
    def __get_token():
        token_path = CONFIG['PATH']['TOKEN']

        # 토큰 획득
        with open(token_path, "r", encoding="utf-8") as tf:
            return tf.read()

    async def print_message(self):
        await self.stdout.send("1분마다 발송되는 메시지")

    async def on_connect(self):
        print("아늑이가 깨어났습니다!")

    async def on_disconnect(self):
        print("아늑이가 떠났습니다...")

    async def on_error(self, err, *args, **kwargs):
        # err는 문자열의 에러메시지
        if err == "on_command_error":
            channel = args[0]
            await channel.send("Something went wrong")

    async def on_command_error(self, context, exception):
        if isinstance(exception, CommandNotFound):
            await context.send("Wrong Command")
        elif hasattr(exception, "original"):
            raise exception.original
        else:
            raise exception

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.stdout = self.get_channel(878239436381495340)

            self.scheduler.start()
            self.scheduler.add_job(self.print_message, CronTrigger(second="0, 30"))
            self.guild = self.get_guild(878239436381495336)

            embed = Embed(title="정신차림", description="아늑이가 깨어났습니다!",
                          color=0xFFDA00, timestamp=datetime.utcnow())
            fields = [("Name", "Value", True),
                      ("Field2", "Second one", False),
                      ("Field3", "Not Inline", False)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            embed.set_author(name="COTIDIE", icon_url=self.guild.icon_url)
            embed.set_thumbnail(url=self.guild.icon_url)
            embed.set_image(url=self.guild.icon_url)
            embed.set_footer(text="This is Footer!")

            await self.stdout.send(embed=embed)
            # 파일 전송
            # await channel.send(file=File("filepath"))

            print("아늑이가 준비를 마쳤습니다!")
        else:
            print("아늑이가 아직 정신을 못차렸습니다.")

    async def on_message(self, message: str):
        pass


# 봇 인스턴스 생성
bot = Bot()
