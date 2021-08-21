import asyncio
from discord.ext.commands.cog import Cog
from discord.ext import commands

"""
    가이드 및 정보 안내를 위한 명령어 Cog
"""


class GuideCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="초보자가이드")
    async def show_guide(self):
        self.bot.stdout.send("초보자가이드입니다.")


def setup(bot):
    bot.add_cog(GuideCog(bot))
