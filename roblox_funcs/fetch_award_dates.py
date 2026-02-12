from bot_managment.aiohttpSessionSetup import get_session
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
    # Do not start the window on construction; start when the first
    # request is made so the countdown is relative to request activity.
    self.reset_time = None
    self.lock = asyncio.Lock()

  async def acquire(self):
    # Loop until a slot can be consumed. Reset and sleep checks are
    # performed under the lock but sleeping is done outside the lock
    # so other coroutines are not blocked.
    while True:
      async with self.lock:
        now = time.time()

        # If a window was started and it's expired, reset and clear
        # the reset_time so the next request will start a new window.
        if self.reset_time is not None and now >= self.reset_time:
          self.remaining = self.max_requests
          self.reset_time = None
          print("🔄 Rate window reset!")

        # If we have quota available, ensure the window is started
        # from this request (if not already) and consume one slot.
        if self.remaining > 0:
          if self.reset_time is None:
            self.reset_time = now + self.window_seconds
          self.remaining -= 1
          return self.remaining

        # No quota left; compute how long until reset. If reset_time
        # is None (shouldn't normally happen), wait a full window.
        sleep_time = (self.reset_time - now) if self.reset_time is not None else self.window_seconds

      # Sleep outside the lock so other coroutines can run and observe state.
      if sleep_time > 0:
        print(f"⏳ Out of quota, waiting {sleep_time:.1f}s for reset...")
        await asyncio.sleep(max(sleep_time, 1))
      else:
        await asyncio.sleep(0.1)

RATE_MANAGER = RateManager(MAX_REQUESTS, RATE_WINDOW)

async def fetch_award_dates(user_id: str, badges: dict, sem, rate_mgr: RateManager) -> list[str]:
  dates = []
  badge_ids = list(badges.values())
  url = f"https://badges.roblox.com/v1/users/{user_id}/badges/awarded-dates"
  STEP = 100
  session = await get_session()
  async with sem:
    for i in range(0, len(badge_ids), STEP):
      params = {"badgeIds": badge_ids[i:i + STEP]}
      headers = {
        "User-Agent": ""
      }

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
  # Use the shared module-level RateManager instance to maintain a single
  # rate window and remaining quota across all concurrent fetches.
  rate_mgr = RATE_MANAGER

  tasks = [
    fetch_award_dates(user_data["user_id"], user_data["badges"], sem, rate_mgr)
    for user_data in user_badges if user_data.get("badges")
  ]
  results = await asyncio.gather(*tasks)
  return results