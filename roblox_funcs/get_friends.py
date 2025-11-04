import aiohttp
import asyncio

async def get_friends(user_id, session, sem):
    url = f"https://friends.roblox.com/v1/users/{user_id}/friends"
    async with sem:  # limits concurrent requests
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                friends_list = data.get("data", [])
                friends_count = len(friends_list)
                return {
                    "user_id": user_id,
                    "friends": {friend["name"].strip(): friend["id"] for friend in friends_list},
                    "friends_count": friends_count
                }
            return {"user_id": user_id, "friends": {}, "friends_count": 0}

async def fetch_multiple_friends(user_ids, limit=5):
    sem = asyncio.Semaphore(limit)
    async with aiohttp.ClientSession() as session:
        tasks = [get_friends(uid, session, sem) for uid in user_ids]
        return await asyncio.gather(*tasks)