import discord
import yaml
import asyncio
import codecs
import requests

from discord.ext import commands
from cogs.utils import checks

with codecs.open("data/config.yaml", 'r', encoding='utf8') as f:
    conf = yaml.safe_load(f)

class Imdb:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='search')
    async def search(self, ctx, *film):
        """
        Look up information about a movie or TV-Show
        """

        embed = discord.Embed(description="Searching... :mag_right:")
        status_msg = await ctx.send(embed=embed)

        api_key = conf["api"]["omdb"]
        search = requests.get(f"http://www.omdbapi.com/?s={film}&apikey={api_key}").json()
        try:
            best_result_id = search["Search"][0]["imdbID"]
        except:
            embed = discord.Embed(description=":x: Not found", color=0xFF0000)
            await status_msg.edit(embed=embed)
            return

        data = requests.get(f"http://www.omdbapi.com/?i={best_result_id}&apikey={api_key}").json()
        title = data["Title"]
        release_date = data["Released"]
        release_year = data["Year"]
        director = data["Director"]
        genre = data["Genre"]
        rating = data["imdbRating"]
        image = data["Poster"]
        imdb_id = ["imdbID"]
        length = data["Runtime"]
        mediatype = data["Type"]

        embed = discord.Embed(title=f"{title} ({release_year})", color=0x0085ff, url=f"https://www.imdb.com/title/{imdb_id}/")
        embed.set_thumbnail(url=image)
        embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        embed.description = director
        embed.add_field(name="Type", value=mediatype.title())
        embed.add_field(name="Genre", value=genre)
        embed.add_field(name="Runtime", value=length)
        embed.add_field(name="IMDb Rating", value=f"{rating}/10")
        embed.set_footer(text=f"Released: {release_date}")

        await status_msg.edit(embed=embed)


def setup(bot):
    bot.add_cog(Imdb(bot))
