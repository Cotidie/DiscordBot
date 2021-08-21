from discord.ext.commands import Cog

class CogBase(Cog):
    def __init__(self, bot, db, scheduler):
        self.bot = bot
        self.db = db
        self.scheduler = scheduler