import os
import json

if os.path.exists("registered_guilds.json"):
  with open("registered_guilds.json", "r") as f:
    registered_guilds = json.load(f) # Loads the json file into a python dictionary.
else:
  registered_guilds = {}

def register_role_with_guild():
  with open("registered_guilds.json", "w") as f:
    json.dump(registered_guilds, f, indent=4) # Dumps the python dictionary into the json file.