import sys
# discord.py
from discord.ext.commands.cog import Cog
from discord.ext.commands     import command

# 커스텀
from lib.helpers.resource import ResourceManager


class BotCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="서버종료")
    async def quit(self, ctx):
        print("서버를 종료합니다.")

        # 자원 회수 및 종료
        ResourceManager.instance().close_all(); print("자원 회수 완료")
        sys.exit()


def setup(bot):
    bot.add_cog(BotCog(bot))