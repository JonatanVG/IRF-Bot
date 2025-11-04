## has_correct_roles: This is a incredibly useful function. You can use this within a command and it will check if the user has any of the "Authorized" roles within registered_guilds. If not the command is killed.
def has_correct_roles(ctx, registered_guilds):
    # Get the guild ID as a string
    guild_id = str(ctx.guild.id)
    
    # Retrieve the set of role IDs associated with the guild from registered_guilds
    role_ids = set(registered_guilds.get(guild_id, {}).get("role_perms", []))
    
    # Get the set of role IDs that the user has
    user_roles = {role.id for role in ctx.author.roles}
    
    # Check if the user has any of the correct roles
    return not role_ids.isdisjoint(user_roles)