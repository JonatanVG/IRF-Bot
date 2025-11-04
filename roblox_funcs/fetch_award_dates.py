import aiohttp
import asyncio
import random

PRINT_PROGRESS = True
BATCH_PER_PRINT = 1000

async def fetch_award_dates(user_id: str, badges: list[dict], session, sem) -> list[str]:
    """
    Make requests to Roblox's Badge API to get user's badge awarded dates
    """
    dates = []
    badge_ids = list(badges.values())
    url = f"https://badges.roblox.com/v1/users/{user_id}/badges/awarded-dates"
    STEP = 75  # Adjust the step size as needed, we can't do too many at once
    async with sem:
        for i in range(0, len(badge_ids), STEP):
            params = {"badgeIds": badge_ids[i:i + STEP]}

            # If we get a 429 status, wait and retry with some backoff
            retry_after = 1
            while True:
                try:
                    async with session.get(url, params=params) as response:
                        if response.status == 429:
                            retry_after = min(retry_after * 1.5, 60)
                            STEP = max(10, int(STEP * 0.8))
                            print(f"Rate limited for user {user_id}. "
                                  f"Sleeping {retry_after}s, STEP={STEP}")
                            await asyncio.sleep(retry_after)
                            continue
                        if response.status != 200:
                            print(f"Error fetching award dates for {user_id}: HTTP {response.status}, skipping batch.")
                            break
                        
                        data = await response.json()

                        for badge in data.get("data", []):
                            dates.append(badge["awardedDate"])

                        await asyncio.sleep(random.uniform(0.8, 1.3))

                        STEP = min(50, int(STEP * 1.1))
                        retry_after = 2
                        print(f"Success: STEP={STEP}, retry_after={retry_after}")
                        break
                except Exception as e:
                    print(f"Exception fetching award dates for {user_id}: {e}")
                    await asyncio.sleep(2)
                    continue
    return dates
                
async def fetch_multiple_award_dates(user_badges: list[dict], limit=5):
    sem = asyncio.Semaphore(limit)
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_award_dates(user_data["user_id"], user_data["badges"], session, sem) 
            for user_data in user_badges if user_data.get("badges")
        ]
        results = await asyncio.gather(*tasks, return_exceptions=False)
        return results