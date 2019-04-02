import discord


from discord.ext import commands
from cogs.utils import checks


class MovieNight(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='movie')
    async def movie(self, ctx, melk):
        await ctx.send(melk)


def setup(bot):
    bot.add_cog(MovieNight(bot))
