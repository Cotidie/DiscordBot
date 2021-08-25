# 스탠다드 라이브러리
from datetime import date

# discord.py
from discord.ext.commands.cog import Cog
from discord.ext.commands import command
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

# 커스텀 객체
from lib.scrapers.sigkill import sigkill_scraper
from lib.bot import GUILD
from lib.db import DB

# 관련 메소드가 많아지면 helper > option.py로 분리
def create_raid_option():
    """
    레이드 정보 선택을 위한 옵션을 반환
    :return: create_option()의 반환값
    """
    choices = [create_choice(
        name="현재",
        value="현재"
    )]
    for boss in DB.get_raid_bosses():
        choices.append(create_choice(
            name=boss,
            value=boss
        ))

    option = create_option(
        name="boss",
        description="어떤 레이드 보스를 알려드릴까요?",
        required=True,
        option_type=3,
        choices=choices
    )

    return option


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

    # TODO: 옵션 설정 부분 Formatter로 분리
    @cog_ext.cog_slash(name="레이드",
                       guild_ids=[GUILD],
                       options=[create_raid_option()])
    async def show_raid_info(self, ctx: SlashContext, boss: str):
        """
            레이드 보스 정보를 불러올게요!
        """
        if boss == "현재":
            await ctx.send("아직 이 기능은 지원하지 않아요 ;_;")
            return

        boss_info = self.bot.db.get_raid_boss(boss)
        embed = self.bot.messenger.embed_raid_info(boss_info)

        await ctx.send(embed=embed)

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
