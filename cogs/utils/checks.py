import discord
from discord.ext import commands


async def check_guild_permissions(ctx, perms, *, check=all):
    is_owner = await ctx.bot.is_owner(ctx.author)
    if is_owner:
        return True

    if ctx.guild is None:
        return False

    resolved = ctx.author.guild_permissions
    return check(getattr(resolved, name, None) == value for name, value in perms.items())


def has_role(ctx, role):
    if ctx.channel is discord.DMChannel:
        return False

    role = discord.utils.get(ctx.author.roles, name=role)
    return role is not None


def has_guild_permissions(*, check=all, **perms):
    async def pred(ctx):
        return await check_guild_permissions(ctx, perms, check=check)
    return commands.check(pred)


def is_even():
    def predicate(ctx):
        return ctx.author.id == 142212883512557569
    return commands.check(predicate)


def is_owner():
    def predicate(ctx):
        owners = [120970603556503552, 142212883512557569, 212635519706726410, 170506717140877312]
        if ctx.author.id in owners:
            return is_owner

    return commands.check(predicate)


def is_admin():
    async def pred(ctx):
        return await check_guild_permissions(ctx, {'administrator': True})
    return commands.check(pred)


def is_mod():
    async def pred(ctx):
        modrole = ctx.bot.settings.get(ctx.guild, 'roles.moderator', 'default_mod')
        return has_role(ctx, modrole)
    return commands.check(pred)


def has_role_id(ctx, role_id):
    if ctx.channel is discord.DMChannel:
        return False

    role = discord.utils.get(ctx.author.roles, id=role_id)
    return role is not None
