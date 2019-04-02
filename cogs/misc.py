import discord
import os
import asyncio
import time
import random
import platform

from discord.ext import commands
from cogs.utils import checks


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping', hidden=True)
    async def _ping(self, ctx):
            start = time.perf_counter()
            message = await ctx.send('Ping...')
            end = time.perf_counter()
            duration = int((end - start) * 1000)
            edit = f'Pong!\nPing: {duration}ms' \
                + f' | websocket: {int(self.bot.latency * 1000)}ms'
            await message.edit(content=edit)

    @commands.command(name='uptime', hidden=True)
    async def _uptime(self, ctx):
        now = time.time()
        diff = int(now - self.bot.uptime)
        days, remainder = divmod(diff, 24 * 60 * 60)
        hours, remainder = divmod(remainder, 60 * 60)
        minutes, seconds = divmod(remainder, 60)
        await ctx.send(f'{days}d {hours}h {minutes}m {seconds}s')

    @commands.command(name='guilds')
    @checks.is_owner()
    async def _guilds(self, ctx):
        guilds = f"{self.bot.user.name} is in:\n"
        for guild in self.bot.guilds:
            guilds += f"{guild.name}\n"
        await ctx.send(guilds)

    @commands.command()
    async def info(self, ctx):
        """
        Info om Filmkveldbot
        """
        membercount = []
        for guild in self.bot.guilds:
            for member in guild.members:
                if member.id in membercount:
                    pass
                else:
                    membercount.append(member.id)
        guilds = len(self.bot.guilds)
        members = len(membercount)
        now = time.time()
        diff = int(now - self.bot.uptime)
        days, remainder = divmod(diff, 24 * 60 * 60)
        hours, remainder = divmod(remainder, 60 * 60)
        minutes, seconds = divmod(remainder, 60)
        avatar = self.bot.user.avatar_url_as(format=None,
                                                static_format='png',
                                                size=1024)

        uptimetext = f'{days}d {hours}t {minutes}m {seconds}s'
        embed = discord.Embed(color=ctx.me.color)
        embed.set_author(name=self.bot.user.name, icon_url=avatar)
        embed.set_thumbnail(url=avatar)
        embed.add_field(name="What?",
                        value="MovieNight bot written for use on /r/Norge's Discord Servers. It's open source! "
                              "You can find it [HERE](https://github.com/Ev-1/ShiteMusicBot)",
                        inline=False)
        embed.set_footer(
            icon_url="https://cdn.discordapp.com/icons/532176350019321917/92f43a1f67308a99a30c169db4b671dd.png?size=64",
            text="{Made by /r/Norge, for /r/Norge}")
        embed.add_field(name="How?",
                        value=f'**Python:** [{platform.python_version()}](https://www.python.org/)'
                        f'\n**Discord.py:** [{discord.__version__}](https://github.com/Rapptz/discord.py/tree/rewrite)')
        embed.add_field(name="How many?",
                        value=f'**Guilds:** {guilds}\n**Users:** {members}')
        embed.add_field(name="How long?",
                        value=uptimetext)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Misc(bot))
