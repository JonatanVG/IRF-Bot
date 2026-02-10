from bot_managment.bot_setup import bot

## Shutdown: Shuts down the bot.
async def shutdown(ctx, name: str = ""):
  if bot.user.name == name:
    await ctx.send("Shutting down...") # Sends a message on discord that the bot is shutting down.
    print("Shutting down...") # This is important to make sure the bot doesn't relaunch. (Only necessary if you're using github actions.)
    await bot.close() # Shuts down the bot.
  else:
    None