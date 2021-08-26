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
               "채팅창에 '/'를 입력하면 저를 이용하실 수 있어요. \n\n" + \
               "제 해부도(?)를 보시려면 [여기](https://github.com/Cotidie/DiscordBot)를 클릭하세요.\n"
        embed = Embed(title="아늑이!", description=desc,
                      color=self.color)

        # 나이 계산(timedelta)
        my_age = date.today() - self.bot.birth

        # 각 필드
        fields = [("이름", "아늑이", True),
                  ("기능", "정보수집", True),
                  ("나이", f"{my_age.days}일", True),
                  ("성장중", "아직 성장중이에요.\n성숙할 수 있도록 많은 아이디어 부탁드려요.", False)]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        # 우측 상단 썸네일
        embed.set_thumbnail(url=self.image)

        # 꼬리말
        embed.set_footer(text="아늑이 by 코티디에 - ALPHA")

        return embed

    def change_status(self, state):
        pass

    def embed_raid_info(self, boss: dict):
        """
         레이드 보스의 정보를 디스코드 Embed로 가공한다
        :param boss: (dict) 필드 정보는 MongoDB > raid_info 컬렉션에서 확인 가능
        :return: (discord.Embed) 보스 정보가 담긴 embed
        """
        from lib.helpers import Formatter   # Circular import 문제. 구조 수정할 필요 있음.

        embed = Embed(title="레이드 보스 정보", color=self.color)
        embed.set_author(name=boss['name'], icon_url=boss['icon'])
        embed.set_footer(text=f"기준일 - {boss['update']}")

        # 출현 시간
        weekday = Formatter.make_unordered_list(boss['weekday'], "-")
        weekend = Formatter.make_unordered_list(boss['weekend'], "-")
        rewards = Formatter.make_unordered_list(boss['reward'], "-")

        # 필드  추가
        fields = [
            (":map: 출현지역", boss['location'], False),
            (":calendar: 주중(월~금)", weekday, True),
            (":calendar: 주말(토,일)", weekend, True),
            (":moneybag: 주요 보상", rewards, False),
            (":link: 참고 링크", f"[싴갤러스]({boss['link']})", False)
        ]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        # 이미지 추가
        embed.set_thumbnail(url=boss['icon'])
        embed.set_image(url=boss['map'][0])

        return embed
