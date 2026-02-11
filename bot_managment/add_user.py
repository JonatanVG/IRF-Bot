import discord
from bot_managment.supabase_setup import Supabase
from bot_managment.bot_setup import bot
from bot_managment.user_authorized import user_authorized
async def add_user(ctx, bot_name: str, user: discord.User):
  if bot.user.name == bot_name:
    # Check if the user is in the database
    if user_authorized(user.id):
      await ctx.send(f"{user.mention} is already in the database with permissions.")
      return
    # If the user is not in the database, add them
    insert_response = (
      Supabase
      .table("AUTHORIZED_BOT_USERS")
      .insert({
        "USERNAME": user.name,
        "USER_ID": user.id
      })
      .execute()
    )
    await ctx.send(f"{user.mention} has been added to the database with permissions.")