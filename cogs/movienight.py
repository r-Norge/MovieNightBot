from discord.ext import commands


class MovieNight(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='movie')
    async def movie(self, ctx):
        """
        yeet
        """
        await ctx.send('yeet')


def setup(bot):
    bot.add_cog(MovieNight(bot))
