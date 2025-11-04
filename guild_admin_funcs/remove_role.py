import discord
from bot_managment.bot_setup import bot
from guild_funcs.register_role_with_guild import register_role_with_guild, registered_guilds

async def remove_role(ctx, role: discord.Role, name: str = ""):
    guild_id = str(ctx.guild.id)
    if bot.user.name == name:
        if guild_id not in registered_guilds:
            registered_guilds[guild_id] = {"role_perms": []}
        if role.id not in registered_guilds[guild_id]["role_perms"]:
            await ctx.send(f"Did not remove [{role}] from role_perms as [{role}] is not present within role_perms.")
            return
        else:
            registered_guilds[guild_id]["role_perms"].remove(role.id)
            await ctx.send(f"Removed [{role}] from role_perms successfully.")
        print(registered_guilds)
    else:
        None