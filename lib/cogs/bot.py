import sys
# discord.py
from discord.ext.commands.cog import Cog
from discord.ext.commands     import command
from discord_slash            import cog_ext, SlashContext

# 커스텀
from lib.helpers import ResourceManager
from lib.bot     import GUILD


class BotCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="자기소개", guild_ids=[GUILD])
    async def introduce(self, ctx: SlashContext):
        """
            저를 소개할게요!
        """
        intro = self.bot.messenger.introduce_self()

        await ctx.send(embed=intro)

    @command(name="서버종료")
    async def quit(self, ctx):
        print("서버를 종료합니다.")

        # 자원 회수 및 종료
        ResourceManager.instance().close_all(); print("자원 회수 완료")
        sys.exit()


def setup(bot):
    bot.add_cog(BotCog(bot))