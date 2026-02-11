import discord
from bot_managment.bot_setup import bot
from guild_funcs.register_role_with_guild import register_role_with_guild, registered_guilds

## Add_role: Adds roles that gain a permit to use the supabase discord bot commands. !!!ONLY USABLE BY THE GUILD/GROUP OWNER!!!
async def add_role(ctx, role: discord.Role, name: str):
  guild_id = str(ctx.guild.id)
  if bot.user.name == name:
    if guild_id not in registered_guilds:
      registered_guilds[guild_id] = {"role_perms": []}
    if role.id not in registered_guilds[guild_id]["role_perms"]:
      registered_guilds[guild_id]["role_perms"].append(role.id)
      register_role_with_guild()
      await ctx.send(f"Added role {role.name} ({role.id}) to the list.")
    else:
      await ctx.send(f"Role {role.name} is already registered.")
    print(registered_guilds)
  else:
    None