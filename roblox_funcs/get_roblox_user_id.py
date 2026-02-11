import aiohttp
import asyncio
from roblox_funcs.get_general_usr_info import get_general_usr_info

async def get_roblox_user_id(username, session, sem):
  url = f"https://users.roblox.com/v1/usernames/users"
  payload = {
    "usernames": [username],
    "excludeBannedUsers": True
  }
  async with sem:
    async with session.post(url, json=payload) as response:
      if response.status == 200:
        data = await response.json()
        if data.get("data"):
          user_info = data["data"][0]
          user_id = user_info["id"]

          user_details = await get_general_usr_info(user_id, sem, session)

          return {
            "username": user_info["requestedUsername"],
            "id": user_id,
            "join_date": user_details.get("join_date"),
            "followers_count": user_details.get("followers_count"),
            "following_count": user_details.get("following_count"),
            "groups_count": user_details.get("groups_count")
          }
      return {
        "username": username,
        "id": None,
        "join_date": None,
        "followers_count": None,
        "following_count": None,
        "groups_count": None
      }

async def fetch_multiple_ids(user_names, limit=5):
  sem = asyncio.Semaphore(limit)
  async with aiohttp.ClientSession() as session:
    tasks = [get_roblox_user_id(uname, session, sem) for uname in user_names]
    return await asyncio.gather(*tasks)