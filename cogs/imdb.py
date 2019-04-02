import discord
import yaml
import asyncio
import codecs
import requests
import urllib.parse

from discord.ext import commands
from cogs.utils import checks


with codecs.open("data/config.yaml", 'r', encoding='utf8') as f:
    conf = yaml.safe_load(f)
    api_key = conf["api"]["omdb"]


async def error_notfound(ctx, status_msg):
    embed = discord.Embed(description=":x: Not found", color=0xFF0000)
    await status_msg.edit(embed=embed)


class Imdb(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name='search', aliases=[''])
    async def search(self, ctx, *film):
        """
        Look up information about a movie or TV-Show
        """

        embed = discord.Embed(description="Searching... :mag_right:")
        status_msg = await ctx.send(embed=embed)
        
        url = "http://www.omdbapi.com/?" + urllib.parse.urlencode({"s": film, "apikey": api_key})
        search = requests.get(url).json()

        try:
            best_result_id = search["Search"][0]["imdbID"]
        except KeyError:
            await error_notfound(ctx, status_msg)
            return

        data = requests.get(f"http://www.omdbapi.com/?i={best_result_id}&apikey={api_key}").json()

        acceptable_media_types = ["movie", "series", "episode"]
        mediatype = data["Type"]
        if mediatype not in acceptable_media_types:
            await error_notfound(ctx, status_msg)
            return

        title = data["Title"]
        release_date = data["Released"]
        release_year = data["Year"]
        director = data["Director"]
        genre = data["Genre"]
        rating = data["imdbRating"]
        image = data["Poster"]
        imdb_id = data["imdbID"]
        length = data["Runtime"]
        plot = data["Plot"]

        embed = discord.Embed(title=f"{title} ({release_year})", color=0x0085ff, url=f"https://www.imdb.com/title/{imdb_id}/")
        embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        embed.add_field(name="Type", value=mediatype.title())
        embed.add_field(name="Genre", value=genre)
        embed.add_field(name="Runtime", value=length)
        embed.add_field(name="IMDb Rating", value=f"{rating}/10")
        embed.set_footer(text=f"Released: {release_date}")

        if not image == "N/A":
            embed.set_thumbnail(url=image)
        if not plot == "N/A" and len(plot) < 1024:
            embed.add_field(name="Plot", value=plot, inline=False)
        if not director == "N/A":
            embed.description = director

        await status_msg.edit(embed=embed)


def setup(bot):
    bot.add_cog(Imdb(bot))
