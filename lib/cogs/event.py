import asyncio
from discord.ext.commands.cog import Cog
from discord.ext.commands     import command


class ActionCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    # 등록 클래스 정의 필요
    @command(name="이벤트등록", aliases=["이벤트_등록"])
    async def register_event(self, ctx):
        await ctx.send("등록할 이벤트 입력")

    def show_notice(self):
        pass

    def show_event(self):
        pass

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