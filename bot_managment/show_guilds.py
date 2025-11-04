from bot_managment.bot_setup import bot
from guild_funcs.register_role_with_guild import registered_guilds

## Show_guilds: Shows all the guilds the bot is in.
async def show_guilds(ctx, name: str = ""):
    if bot.user.name == name:
        guild_ids = list(registered_guilds.keys()) # Gets the guild IDs from registered_guilds.
        guild_names = [bot.get_guild(int(guild_id)).name for guild_id in guild_ids if bot.get_guild(int(guild_id))]
        await ctx.send(f"Registered Guilds: {guild_names}") # Sends the name of every guild the bot is in.
    else:
        None