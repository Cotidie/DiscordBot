import asyncio
# discord.py
from discord.ext.commands.cog import Cog
from discord.ext.commands     import command

# 커스텀 객체
from lib.scrapers.sigkill import sigkill_scraper


class ActionCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    # 등록 클래스 정의 필요
    @command(name="이벤트등록", aliases=["이벤트_등록"])
    async def register_event(self, ctx):
        await ctx.send("등록할 이벤트 입력")

    def show_notice(self):
        pass

    @command(name="오늘의미션")
    async def show_today_event(self, ctx):
        """
            * 정보출처: https://mabi.sigkill.kr/todaymission/
            * 동작: 위 페이지를 스크레이핑하여 오늘의 미션 목록을 출력합니다.
        """
        result = "오늘의 미션 정보입니다. \n" + \
                 "정보출처: https://mabi.sigkill.kr/ \n\n"

        # 오늘의 미션 정보 얻기
        events = sigkill_scraper.get_today_events()
        for event in events:
            result += event + "\n"

        await ctx.send(result)

    def show_official_notice(self):
        pass

    def show_official_event(self):
        pass

    def show_guild_notice(self):
        pass

    def show_guild_event(self):
        pass

def setup(bot):
    bot.add_cog(ActionCog(bot))