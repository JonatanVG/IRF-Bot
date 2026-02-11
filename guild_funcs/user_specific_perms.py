import discord
from discord.ext import commands
from discord import app_commands
from bot_managment.supabase_setup import Supabase as supabase
# This function checks if a user has specific permissions in the database. 
# It returns True if the user has permissions, and False otherwise.
def user_specific_perms():
  async def slash_predicate(inter: discord.Interaction) -> bool:
    user_id = inter.user.id
    response = (
      supabase.table("AUTHORIZED_BOT_USERS")
      .select("*")
      .eq("USER_ID", user_id)
      .execute()
    )
    await inter.response.defer() # Defer the response to give the bot more time to check the database.
    if bool(response.data) == False:
      await inter.followup.send("You do not have permission to use this command. Please contact the bot administrator for more information.")
    return bool(response.data)
  async def prefix_predicate(ctx: commands.Context) -> bool:
    user_id = ctx.author.id
    response = (
      supabase.table("AUTHORIZED_BOT_USERS")
      .select("*")
      .eq("USER_ID", user_id)
      .execute()
    )
    await ctx.defer() # Defer the response to give the bot more time to check the database.
    if bool(response.data) == False:
      await ctx.send("You do not have permission to use this command. Please contact the bot administrator for more information.")
    return bool(response.data)
  def decorator(func):
    func = app_commands.check(slash_predicate)(func)
    func = commands.check(prefix_predicate)(func)
    return func
  return decorator