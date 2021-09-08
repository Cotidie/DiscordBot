import asyncio
from discord.ext.commands.cog import Cog
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

from lib.bot            import GUILDS
from lib.helpers        import Formatter, OptionMaker
"""
    가이드 및 정보 안내를 위한 명령어 Cog
"""


class GuideCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="오늘의혜택",
                       guild_ids=GUILDS,
                       options=OptionMaker.today_effect_options())
    async def show_today_effect(self, ctx: SlashContext, which: str, day: int):
        """
            요일별 혜택을 알려드릴게요!
        """
        if day == -1:
            day = Formatter.get_korean_time('date').weekday()

        if which == '어드밴스드':
            await ctx.send("이 기능은 아직 준비중이에요 ;_;")
        elif which == '요일':
            await ctx.send("이 기능은 아직 준비중이에요 ;_;")

    @commands.command(name="초보자가이드")
    async def show_guide(self, ctx):
        await ctx.send("초보자가이드입니다.")


def setup(bot):
    bot.add_cog(GuideCog(bot))
