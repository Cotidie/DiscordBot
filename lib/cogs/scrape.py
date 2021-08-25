# 스탠다드 라이브러리
from datetime import date

# discord.py
from discord.ext.commands.cog import Cog
from discord.ext.commands     import command
from discord_slash            import cog_ext, SlashContext

# 커스텀 객체
from lib.scrapers.sigkill import sigkill_scraper
from lib.bot              import GUILD


class ScrapeCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    # # 등록 클래스 정의 필요
    # @cog_ext.cog_slash(name="이벤트등록", guild_ids=[878239436381495336])
    # async def register_event(self, ctx):
    #     await ctx.send("등록할 이벤트 입력")

    def show_notice(self):
        pass

    @cog_ext.cog_slash(name="오늘의미션", guild_ids=[GUILD])
    async def show_today_event(self, ctx: SlashContext):
        """
            오늘의 미션 목록을 불러올게요!
        """
        result = f"오늘의 미션 정보입니다. ({date.today()})\n" + \
                 "정보출처: https://mabi.sigkill.kr/ \n\n"

        # 오늘의 미션 정보 얻기
        events = sigkill_scraper.get_today_missions()
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
    bot.add_cog(ScrapeCog(bot))