import discord
from bot_managment.supabase_setup import Supabase
from bot_managment.bot_setup import bot
from bot_managment.user_authorized import user_authorized
async def remove_user(ctx, bot_name: str, user: discord.User):
  if bot.user.name == bot_name:
    # Check if the user is in the database
    if not user_authorized(user.id):
      await ctx.send(f"{user.mention} is not in the database with permissions.")
      return
    # If the user is in the database, remove them
    delete_response = (
      Supabase
      .table("AUTHORIZED_BOT_USERS")
      .delete()
      .eq("USER_ID", user.id)
      .execute()
    )
    await ctx.send(f"{user.mention} has been removed from the database with permissions.")