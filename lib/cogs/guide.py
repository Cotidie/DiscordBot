import asyncio
from discord.ext.commands.cog import Cog
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

from lib.bot            import GUILDS
from lib.db             import DB
from lib.helpers        import Formatter
from lib.helpers.option import OptionMaker
"""
    가이드 및 정보 안내를 위한 명령어 Cog
"""


class GuideCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="오늘의효과",
                       guild_ids=GUILDS,
                       options=OptionMaker.today_effect_options())
    async def show_today_effect(self, ctx: SlashContext, day: int):
        """
            요일별 효과를 알려드릴게요!
        """
        if day == -1:
            today = Formatter.get_korean_time('datetime')
            day = today.weekday()
            # 오전 7시 이전이면 1을 뺀다
            if today.hour < 7:
                day = 6 if day == 0 else day-1

        info = DB.get_day_effect(day)
        embed = self.bot.messenger.embed_day_effect(info)
        await ctx.send(embed=embed)

    @commands.command(name="초보자가이드")
    async def show_guide(self, ctx):
        await ctx.send("초보자가이드입니다.")


def setup(bot):
    bot.add_cog(GuideCog(bot))
