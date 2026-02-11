import aiohttp
import asyncio
import requests

PRINT_PROGRESS = True
BATCH_PER_PRINT = 1000

async def fetch_badges(user_id: str, session, sem) -> dict:
  """
  Given a Roblox user id, get the user's badge data.
  """
  badges = {}
  cursor = None
  async with sem:
    while True:
      url = f"https://badges.roblox.com/v1/users/{user_id}/badges?limit=100&sortOrder=Desc"
      if cursor:
        url += f"&cursor={cursor}"
      async with session.get(url) as response:
        if response.status == 200:
          data = await response.json()
          for badge in data.get("data", []):
            badges[badge["name"].strip()] = badge["id"]
          cursor = data.get("nextPageCursor")
          if not cursor:
            break
        else:
          break
  return {"user_id": user_id, "badges": badges}

async def fetch_multiple_users_badges(user_ids, limit=5):
  sem = asyncio.Semaphore(limit)
  async with aiohttp.ClientSession() as session:
    tasks = [fetch_badges(uid, session, sem) for uid in user_ids]
    return await asyncio.gather(*tasks)