async def get_usernames_from_ids(user_ids: list[int], session):
  if not user_ids:
    return {}
  url = "https://users.roblox.com/v1/users"
  async with session.post(url, json={"userIds": user_ids}) as response:
    if response.status == 200:
      data = await response.json()
      return {u["id"]: u for u in data.get("data", [])}
    return {}