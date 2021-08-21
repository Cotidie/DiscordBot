from datetime import datetime

from discord import Intents, Embed, File
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from ..db import db

"""
    * self.get_server(ID): 속한 서버, 하드코딩됨
    * self.get_channel(ID): 속한 채널, 하드코딩됨
    * 리팩토링: ChatManager, ErrorHandler, Handlers > Event, Command
    * 필요기능: 오늘의 이벤트, 
"""


# 봇이 반응할 접두사
PREFIX = "!"
OWNER_IDS = [525193576716566528]

class Bot(BotBase):
    def __init__(self):
        self.PREFIX     = PREFIX    # 봇이 반응할 접두사
        self.guild      = None      # 속할 서버
        self.ready      = False
        self.scheduler  = AsyncIOScheduler()    # 코드의 주기적, 예약 수행

        db.autosave(self.scheduler)
        super().__init__(command_prefix=PREFIX,
                         owner_ids=OWNER_IDS,
                         intents=Intents.all())

    def run(self, version:str):
        self.VERSION = version

        # 토큰 획득
        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("아늑 봇이 정신을 차리고 있습니다...")
        super().run(self.TOKEN, reconnect=True)

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
            self.scheduler.start()

            self.guild = self.get_guild(878239436381495336)
            channel = self.get_channel(878239436381495340)
            await channel.send("아늑이가 깨어났습니다!")

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
            await channel.send(embed=embed)
            # 파일 전송
            #await channel.send(file=File("filepath"))


            print("아늑이가 준비를 마쳤습니다!")
        else:
            print("아늑이가 아직 정신을 못차렸습니다.")
    
    async def on_message(self, message:str):
        pass

        

# 봇 인스턴스 생성
bot = Bot()