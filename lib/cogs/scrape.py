# 서드파티
from discord.ext.commands.cog import Cog
from discord.ext.commands import command
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

# 커스텀 객체
from lib.scrapers   import sigkill_scraper, chic_scraper
from lib.db         import DB
from lib.bot        import GUILDS
from lib.helpers    import Formatter


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

    @cog_ext.cog_slash(name="오늘의미션", guild_ids=GUILDS)
    async def show_today_event(self, ctx: SlashContext):
        """
            오늘의 미션 목록을 불러올게요!
        """
        today = Formatter.get_korean_time('date')

        result = f"오늘의 미션 정보입니다. ({today})\n" + \
                 "정보출처: https://mabi.sigkill.kr/ \n\n"

        # 오늘의 미션 정보 얻기
        events = sigkill_scraper.get_today_missions(today)
        if not events:
            await ctx.send("정보를 불러오는 데에 실패했어요 ;_;")
            return

        for event in events:
            result += event + "\n"

        await ctx.send(result)

    # TODO: 옵션 설정 부분 Formatter로 분리
    @cog_ext.cog_slash(name="레이드",
                       guild_ids=GUILDS,
                       options=[create_raid_option()])
    async def show_raid_info(self, ctx: SlashContext, boss: str):
        """
            레이드 보스 정보를 불러올게요!
        """
        # 진행중인 레이드이면 제보된 채널을 스크레이핑한다.
        # '현재'를 선택했는데 진행중인 레이드가 없으면 다음 레이드를 알린다
        # '현재'를 선택했는데 진행중인 레이드가 여러 개이면 페이지 기능을 활용한다
        now = Formatter.get_korean_time('datetime')

        if boss == "현재":
            bosses = self.bot.db.get_current_raids(time=now)
            if not bosses:
                message = "현재 진행중인 레이드가 없어요 ;_; \n"
                await ctx.send(message)
                return

            message = f"현재 {', '.join(bosses)} 출현시간입니다."
            await ctx.send(message)
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

    @command(name="레이드동기화")
    async def syncronize_raid_time(self, ctx):
        """
         싴갤러스의 레이드 시간표와 DB를 동기화한다.
        :return: None
        """
        chic_scraper.syncronize_raid_time()
        await ctx.send("동기화 작업이 완료되었습니다.")

def setup(bot):
    bot.add_cog(ScrapeCog(bot))
