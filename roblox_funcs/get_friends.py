import aiohttp
import asyncio
from roblox_funcs.get_usernames_from_ids import get_usernames_from_ids

async def get_friends(user_id, session: aiohttp.ClientSession, sem: asyncio.Semaphore):
  url = f"https://friends.roblox.com/v1/users/{user_id}/friends"
  async with sem:  # limits concurrent requests
    async with session.get(url) as response:
      if response.status != 200:
        return { "user_id": user_id, "friends": {}, "friends_count": 0 }
      
      data = await response.json()
      friends_list = data.get("data", [])
      friend_ids = [f["id"] for f in friends_list]
      id_to_user = await get_usernames_from_ids(friend_ids, session)
      friends = { info["name"]: fid for fid, info in id_to_user.items() }
      
      return { "user_id": user_id, "friends": friends, "friends_count": len(friends_list) }
    return { "user_id": user_id, "friends": {}, "friends_count": 0 }

async def fetch_multiple_friends(user_ids, limit=5):
  sem = asyncio.Semaphore(limit)
  async with aiohttp.ClientSession() as session:
    tasks = [get_friends(uid, session, sem) for uid in user_ids]
    return await asyncio.gather(*tasks)