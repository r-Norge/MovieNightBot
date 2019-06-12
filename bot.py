import discord
import yaml
import codecs
import time
import sys
import traceback

from discord.ext import commands

from cogs.utils.settings import Settings


with codecs.open('data/config.yaml', 'r', encoding='utf8') as f:
    conf = yaml.safe_load(f)


initial_extensions = [
    'cogs.cogs',
    'cogs.imdb',
    'cogs.misc',
    'cogs.movienight'
]


def _get_prefix(bot, message):
    if not message.guild:
        return bot.settings.default_prefix
    prefixes = bot.settings.get(message.guild, 'prefixes', 'default_prefix')
    return commands.when_mentioned_or(*prefixes)(bot, message)


class Bot(commands.Bot):
    def __init__(self, debug: bool=False):
        super().__init__(command_prefix=_get_prefix,
                         description=conf['bot']['description'])

        self.settings = Settings(**conf['default server settings'])
        self.debug = debug

        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                print(e)

    async def on_command_error(self, ctx, err):
        if not self.debug:
            if (isinstance(err, commands.MissingRequiredArgument) or
                    isinstance(err, commands.BadArgument)):
                await ctx.send_help(ctx.command)

            if isinstance(err, commands.CommandInvokeError):
                pass

            elif isinstance(err, commands.NoPrivateMessage):
                await ctx.send('That command is not available in DMs')

            elif isinstance(err, commands.CommandOnCooldown):
                await ctx.send(
                    f'{ctx.message.author.mention} Command is on cooldown. ' +
                    f'Try again in `{err.retry_after:.1f}` seconds.')

            elif isinstance(err, commands.MissingPermissions):
                permissions = '\n'.join(err.missing_perms)
                return await ctx.send(
                    f'You need the following permissions in order to execute the command\n```{permissions}```')

            elif isinstance(err, commands.BotMissingPermissions):
                permissions = '\n'.join(err.missing_perms)
                return await ctx.send(
                    f'I need the following permissions in order to execute the command\n```{permissions}```')

            elif isinstance(err, commands.CheckFailure):
                pass

            elif isinstance(err, commands.CommandNotFound):
                pass
        else:
            tb = err.__traceback__
            traceback.print_tb(tb)
            print(err)

    async def on_ready(self):
        if not hasattr(self, 'uptime'):
            self.uptime = time.time()
            if self.debug:
                print('\n\nDebug mode')

        print(f'\nLogged in as: {self.user.name}' +
              f' in {len(self.guilds)} servers.')
        print(f'Version: {discord.__version__}\n')

        await self.change_presence(activity=discord.Game(type=0,
                                   name=conf['bot']['playing status']),
                                   status=discord.Status.online)

    def run(self):
        try:
            super().run(conf['bot']['token'], reconnect=True)
        except Exception as e:
            tb = e.__traceback__
            traceback.print_tb(tb)
            print(e)


def run_bot(debug: bool=False):
    bot = Bot(debug=debug)
    bot.run()


if __name__ == '__main__':
    if 'debug' in sys.argv:
        run_bot(debug=True)
    else:
        run_bot(debug=False)
