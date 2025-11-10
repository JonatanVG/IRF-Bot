import aiohttp
import asyncio
import time

PRINT_PROGRESS = True
BATCH_PER_PRINT = 1000
RATE_WINDOW = 70        # Roblox seems to reset every ~90s
MAX_REQUESTS = 10       # Roblox allows ~10 requests per 90s window

class RateManager:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.remaining = max_requests
        self.window_seconds = window_seconds
        self.reset_time = time.time() + window_seconds
        self.lock = asyncio.Lock()

    async def acquire(self):
        async with self.lock:
            now = time.time()
            # Reset if window expired
            if now >= self.reset_time:
                self.remaining = self.max_requests
                self.reset_time = now + self.window_seconds
                print("🔄 Rate window reset!")

            # If no quota left, wait for reset
            while self.remaining <= 0:
                sleep_time = self.reset_time - time.time()
                print(f"⏳ Out of quota, waiting {sleep_time:.1f}s for reset...")
                await asyncio.sleep(max(sleep_time, 1))
                self.remaining = self.max_requests
                self.reset_time = time.time() + self.window_seconds

            # Consume 1 slot
            self.remaining -= 1
            return self.remaining

async def fetch_award_dates(user_id: str, badges: dict, session, sem, rate_mgr: RateManager) -> list[str]:
    dates = []
    badge_ids = list(badges.values())
    url = f"https://badges.roblox.com/v1/users/{user_id}/badges/awarded-dates"
    STEP = 100

    async with sem:
        for i in range(0, len(badge_ids), STEP):
            params = {"badgeIds": badge_ids[i:i + STEP]}

            # Wait for rate quota
            remaining = await rate_mgr.acquire()
            print(f"User {user_id}: {remaining} requests remaining this window")

            try:
                async with session.get(url, params=params) as response:
                    if response.status == 429:
                        print(f"⚠️ Rate limited for user {user_id}. Sleeping 60s.")
                        await asyncio.sleep(60)
                        continue

                    if response.status != 200:
                        print(f"Error fetching award dates for {user_id}: HTTP {response.status}")
                        continue

                    data = await response.json()
                    for badge in data.get("data", []):
                        dates.append(badge["awardedDate"])

                    if PRINT_PROGRESS and len(dates) % BATCH_PER_PRINT == 0:
                        print(f"{len(dates)} awarded dates for {user_id} requested.")

                    await asyncio.sleep(1)  # small delay between requests

            except Exception as e:
                print(f"Exception fetching award dates for {user_id}: {e}")
                await asyncio.sleep(2)
                continue

    return dates

async def fetch_multiple_award_dates(user_badges: list[dict], limit=5):
    sem = asyncio.Semaphore(limit)
    rate_mgr = RateManager(MAX_REQUESTS, RATE_WINDOW)

    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_award_dates(user_data["user_id"], user_data["badges"], session, sem, rate_mgr)
            for user_data in user_badges if user_data.get("badges")
        ]
        results = await asyncio.gather(*tasks)
        return results
