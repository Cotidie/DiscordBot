from discord import Embed
from config import CONFIG
from datetime import date

"""
    봇의 디스코드 채팅을 위한 메시지 빌더
    정해진 형식의 Embed, 문자열 등을 정의합니다.
"""


class Messenger:
    def __init__(self, bot):
        self.bot = bot
        self.color = CONFIG['BOT']['COLOR']
        self.image = CONFIG['BOT']['IMAGE']

    def introduce_self(self):
        """
         최초 서버 접속 및 자기소개 명령어에 쓰일 자기소개 메시지
        :return: (discord.Embed) 내용이 채워진 Embed 객체
        """
        # 상단 설명란
        desc = "에린 세계의 여러 잡일을 도맡아 해드리고 있어요.\n" + \
               "제가 할 수 있는 일은 '!도와줘'를 통해 알 수 있어요. \n\n" + \
               "제 해부도(?)를 보시려면 [여기](https://github.com/Cotidie/DiscordBot)를 클릭하세요.\n"
        embed = Embed(title="아늑이!", description=desc,
                      color=self.color)

        # 나이 계산(timedelta)
        my_age = date.today() - self.bot.birth

        # 각 필드
        fields = [("이름", "아늑이", True),
                  ("기능", "!도와줘", True),
                  ("나이", f"{my_age.days}일", True),
                  ("성장중", "아직 성장중이에요.\n성숙할 수 있도록 많은 아이디어 부탁드려요.", False)]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        # 우측 상단 썸네일
        embed.set_thumbnail(url=self.image)

        # 꼬리말
        embed.set_footer(text="아늑이 - ALPHA")

        return embed

    def change_status(self, state):
        pass
