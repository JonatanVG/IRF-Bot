from guild_funcs.register_role_with_guild import registered_guilds
from bot_managment.bot_setup import bot

## Show_roles: Shows all roles with permission to use the supabase commands in your server.
async def show_roles(ctx, name: str = ""):
  guild_id = str(ctx.guild.id)
  role_ids = registered_guilds.get(guild_id, {}).get("role_perms", [])
  if bot.user.name == name:
    if role_ids:
      # Convert role IDs to role names
      role_names = [ctx.guild.get_role(role_id).name for role_id in role_ids if ctx.guild.get_role(role_id)]
      if role_names:
        await ctx.send(f"Registered roles: {', '.join(role_names)}")
      else:
        await ctx.send("No valid roles found (roles may have been deleted).")
    else:
      await ctx.send("No roles registered for this guild.")
    print(registered_guilds)
  else:
    None