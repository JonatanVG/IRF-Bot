### Import all basic required libraries.
import discord # Import Discord library
from discord import app_commands # Will be needed if you're planning on making / commands
from discord.ext import commands # You need commands, but tasks is only necessary if you want it to for an example execute a function once every 1 hour.
import os # Import os library
from dotenv import load_dotenv # Change import dotenv to this instead.
import threading
### End import libraries.

load_dotenv() # Makes the code able to read the .env file.

### Import guild functions
from guild_funcs.register_role_with_guild import registered_guilds
from guild_funcs.has_correct_roles import has_correct_roles
from guild_funcs.guild_owner_only import guild_owner_only
from guild_funcs.user_specific_perms import user_specific_perms
### End of import guild functions

### Load environment variables
token = os.getenv("BOT_TOKEN") # Write this to access your bots token.
### End of load environment variables

### Import bot
from bot_managment.bot_setup import bot
### End import bot

### Import supabase client
from bot_managment.supabase_setup import Supabase, Supabase2
### End import supabase client


guilds = bot.guilds
guild_names = []


### Bot events
@bot.event 
async def on_ready(): # This runs automatically when your bot starts.
    for guild in guilds:
        guild_names.append(guild.name) # Creates a list of the servers your bot is in.
    print(f'Logged in as {bot.user}')
    print(f'GUILD_ID(S): {guild_names}')
    try:
        synced = await bot.tree.sync() # Syncronizes the tree commands your bot has with all servers it's in.
        print(f"Synced {len(synced)} command(s) globally.")
    except Exception as e:
        print(f"Failed to syn command(s): {e}")

## on_guild_join: This event runs whenever the bot is added to a guild.
@bot.event
async def on_guild_join(guild):
    registered_guilds[str(guild.id)] = {"role_perms": []} # Adds the guild to it's register.
    print(f"Added guild {guild.name} ({guild.id}) to registered_guilds.")
    print(registered_guilds)

## on_guild_remove: This event runs whenever the bot is removed from a guild.
@bot.event
async def on_guild_remove(guild):
    if str(guild.id) in registered_guilds: # If the guild is registered in registered_guilds it continues and deletes the entry.
        del registered_guilds[str(guild.id)]
        print(f"Removed guild {guild.name} ({guild.id}) from registered_guilds.")
    print(registered_guilds)
### End bot events


### Bot commands
## bgc_run: This command runs the background check on the specified user(s).
import roblox_funcs.command_main as command_main
@bot.tree.command(name="bgc_run", description="Runs a background check on the specified user(s).")
@user_specific_perms(Supabase) # This makes so only users with permissions in the database can run this command.
@app_commands.describe(type="Generate award date graph? (Significantly increases time to complete. (+5 secs per 60 badges.))")
@app_commands.choices(type = [
    app_commands.Choice(name="Yes", value="B"),
    app_commands.Choice(name="No", value="A")
])
async def bgc_run(inter: discord.Interaction, usernames: str, type: str):
    usernames_list = [username.strip() for username in usernames.split(",") if username.strip()]
    await command_main.main(inter, usernames_list, type)

## check_database: This command checks if users in a group are in the database.
import missingFromDatabaseChecker.Comparison as bot_funcs
@bot.command(name="compare")
async def compare(ctx, name: str = ""):
    if bot.user.name == name:
        guild_id = ctx.guild.id
        result, Names = await bot_funcs.Comparison(guild_id)
        if result is None:
            await ctx.send("This bot can only be used in specific guilds. Please contact the bot administrator for more information.")
            return
        await ctx.send(f"**Users not in database:**\n{result}\n\n**Usernames:**\n{Names}")
    else:
        None
## Slash command version of compare
@bot.tree.command(name="compare", description="Compares the group members with the sheet data and returns users not in the database.")
async def compare_interaction(inter: discord.Interaction):
    await inter.response.send_message("Processing comparison, please wait...")
    guild_id = inter.guild_id
    result, Names = await bot_funcs.Comparison(guild_id)
    if result is None:
        await inter.channel.send("This bot can only be used in specific guilds. Please contact the bot administrator for more information.")
        return
    await inter.channel.send(f"**Users not in database:**\n{result}\n\n**Usernames:**\n{Names}")
### Bot commands end


### Guild admin commands
## Add_role: Adds roles that then gain permission to use commands locked off by the has_correct_roles function.
import guild_admin_funcs.add_role as add_role_func
@bot.command(name="add_role")
@guild_owner_only()
async def add_role(ctx, role: discord.Role, name: str = ""):
    await add_role_func.add_role(ctx, role, name)

## Remove_role: Removes roles from the permission list removing their command privileges.
import guild_admin_funcs.remove_role as remove_role_func
@bot.command(name="remove_role")
@guild_owner_only()
async def remove_role(ctx, role: discord.Role, name: str = ""):
    await remove_role_func.remove_role(ctx, role, name)

## Show_roles: Shows all roles with command privileges.
import guild_admin_funcs.show_roles as show_roles_func
@bot.command(name="show_roles")
@guild_owner_only()
async def show_roles(ctx, name: str = ""):
    await show_roles_func.show_roles(ctx, name)
### End of guild admin commands


### Bot managment
## add_user: Adds a user to the database with permissions to use commands locked off by the user_specific_perms function.
import bot_managment.add_user as add_user_func
@bot.command(name="add_user")
@commands.is_owner() # Makes so the bot only responds if the user is the owner of the bot.
async def add_user(ctx, bot_name: str, user: discord.User):
    await add_user_func.add_user(ctx, bot_name, user)

## remove_user: Removes a user from the database removing their permissions to use commands locked off by the user_specific_perms function.
import bot_managment.remove_user as remove_user_func
@bot.command(name="remove_user")
@commands.is_owner() # Makes so the bot only responds if the user is the owner of the bot.
async def remove_user(ctx, bot_name: str, user: discord.User):
    await remove_user_func.remove_user(ctx, bot_name, user)

## Shutdown: Shuts down the bot.
import bot_managment.shutdown as shutdown_func
@bot.command(name="shutdown")
@commands.is_owner() # Makes so the bot only responds if the user is the owner of the bot.
async def shutdown(ctx, name: str = ""):
    await shutdown_func.shutdown(ctx, name)

## Ping: Returns the latency of the bot.
import bot_managment.ping as ping_func
@bot.command(name="ping")
async def ping(ctx, name: str = ""):
    await ping_func.ping(ctx, name)

## Restart: Restarts the bot letting it update its source code.
import bot_managment.restart as restart_func
@bot.command(name="restart")
@commands.is_owner() # Make so the bot only responds if the user is the owner of the bot.
async def restart(ctx, name: str = ""):
    await restart_func.restart(ctx, name)

## Show_guilds: Shows all the guilds the bot is in.
import bot_managment.show_guilds as show_guilds_func
@bot.command(name="show_guilds")
@commands.is_owner()
async def show_guilds(ctx, name: str = ""):
    await show_guilds_func.show_guilds(ctx, name)
### End of bot managment

from server.health_server import health_server
from server.keep_alive import keep_alive
threading.Thread(target=health_server, daemon=True).start()
threading.Thread(target=keep_alive, daemon=True).start()

bot.run(token) # Runs the bot.