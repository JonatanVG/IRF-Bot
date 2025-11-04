import os
import sys
from bot_managment.bot_setup import bot

## Restart: Restarts the bot letting it update its source code.
async def restart(ctx, name: str = ""):
    if bot.user.name == name:
        await ctx.send("Restarting...") # Sends a message on discord that the bot is restarting.
        os.execl(sys.executable, sys.executable, *sys.argv) # Kills the current runtime after having made a new one with the updated (or same) source code.
    else:
        None