from datetime import datetime

async def get_general_usr_info(user_id, sem, session):
    async with sem:
        try:
            url = f"https://users.roblox.com/v1/users/{user_id}"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    groups_url = f"https://groups.roblox.com/v1/users/{user_id}/groups/roles"
                    async with session.get(groups_url) as groups_response:
                        groups_count = 0
                        if groups_response.status == 200:
                            groups_data = await groups_response.json()
                            groups_count = len(groups_data.get("data", []))

                    followers_url = f"https://friends.roblox.com/v1/users/{user_id}/followers/count"
                    async with session.get(followers_url) as followers_response:
                        followers_count = 0
                        if followers_response.status == 200:
                            followers_data = await followers_response.json()
                            followers_count = followers_data.get("count", 0)

                    following_url = f"https://friends.roblox.com/v1/users/{user_id}/followings/count"
                    async with session.get(following_url) as following_response:
                        following_count = 0
                        if following_response.status == 200:
                            following_data = await following_response.json()
                            following_count = following_data.get("count", 0)

                    join_date = None
                    if data.get("created"):
                        try:
                            join_date = datetime.fromisoformat(data["created"].replace("Z", "+00:00"))
                        except:
                            join_date = data["created"]

                    return {
                        "join_date": join_date,
                        "followers_count": followers_count,
                        "following_count": following_count,
                        "groups_count": groups_count
                    }
                else:
                    return {}
        except Exception as e:
            print(f"Error fetching details for user {user_id}: {e}")
            return {}