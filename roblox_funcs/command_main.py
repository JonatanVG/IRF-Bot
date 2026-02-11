import discord
import asyncio

from roblox_funcs.get_roblox_user_id import fetch_multiple_ids
from roblox_funcs.get_friends import fetch_multiple_friends
from roblox_funcs.get_trello_blacklist import get_trello_blacklist
from roblox_funcs.check_friends_against_blacklist import check_friends_against_blacklist
from roblox_funcs.fetch_badges import fetch_multiple_users_badges
from roblox_funcs.fetch_award_dates import fetch_multiple_award_dates
from roblox_funcs.plot_cumulative_badges import plot_cumulative_badges

async def main(inter: discord.Interaction, usernames: list[str], type: str):
  notation = []
  img = None

  active = True
  timer = 0

  async def time_loop():
    nonlocal timer
    while active:
      await asyncio.sleep(1)
      timer += 1
  
  timer_task_obj = asyncio.create_task(time_loop())

  await inter.channel.send("Processing users. This may take between 1-10 minutes depending on each users inventory size.")

  print("fetching trello blacklist...")
  blacklist = get_trello_blacklist()
  print(f"Loaded {len(blacklist)} blacklisted names.\n")

  print("Fetching Roblox user IDs...")
  user_id_results = await fetch_multiple_ids(usernames)
  user_ids = [user["id"] for user in user_id_results if user["id"] is not None]
  print(f"Fetched {len(user_ids)} valid user IDs.\n")

  print("Fetching friends for all users...")
  friend_results = await fetch_multiple_friends(user_ids)

  print("Fetching badges for all users...")
  badge_results = await fetch_multiple_users_badges(user_ids)
  badges_map = {b["user_id"]: b["badges"] for b in badge_results}
  for a in user_ids:
    print(f"Badges counted for {a}: {len(badges_map.get(a, {}))}")

  if type == "B":
    print("Fetching award dates for all users...")
    award_date_results = await fetch_multiple_award_dates(badge_results)

    award_dates_map = {}
    for i, user in enumerate(user_id_results):
      user_id = user["id"]
      if i < len(award_date_results):
        award_dates_map[user_id] = award_date_results[i]
      else:
        award_dates_map[user_id] = []

  for user_result in friend_results:
    user_id = user_result["user_id"]
    friends = user_result["friends"]
    friends_count = user_result["friends_count"]
    badges = badges_map.get(user_id, {})

    user_info = next((u for u in user_id_results if u["id"] == user_id), None)
    if not user_info:
      continue

    username = user_info["username"]
    join_date = user_info["join_date"]
    followers = user_info["followers_count"]
    following = user_info["following_count"]
    groups = user_info["groups_count"]

    if type == "B":
      badge_dates = award_dates_map.get(user_id, [])
      img = plot_cumulative_badges(username, user_id, badge_dates)
      print(f"{username} ({username}) has {len(badge_dates)} badge award dates recorded.")

    flagged = check_friends_against_blacklist(friends, blacklist)

    header = f"\n**{username}** ({user_id})"
    notation.append(header)
    print(header)

    user_details = (f"\n**Join date:** {join_date}"
                    f"\n**Friend count:** {friends_count}"
                    f"\n**Follower count:** {followers}"
                    f"\n**Following count:** {following}"
                    f"\n**Group count:** {groups}")
    
    notation.append(user_details)
    print(user_details)

    if flagged:
      notation.append(f"\n⚠️  has blacklisted friends:")
      print(f"\n⚠️  has blacklisted friends:")
      for name, list_type, fid in flagged:
        entry = f"  - {name} ({fid}) → {list_type}"
        notation.append(entry)
        print(entry)
    else:
      notation.append(f"\n✅ No blacklisted friends.")
      print(f"\n✅ No blacklisted friends.")
    
    if badges:
      notation.append(f"🏅  Badges: {len(badges)} total")
      print(f"🏅  Badges: {len(badges)} total")
    else:
      notation.append("🚫  No badges found.")
      print("🚫  No badges found.")

    response = "\n".join(notation)

    if img:
      discord_file = discord.File(img, filename=f"{username}-{user_id}.png")
      await inter.channel.send(response, file=discord_file)
    else:
      await inter.channel.send(response)
        
    notation = []

  active = False
  await timer_task_obj
  await inter.channel.send(f"This request elapsed a total of {timer} seconds.")
  
  print("\nAll users processed.")