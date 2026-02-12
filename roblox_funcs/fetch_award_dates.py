from bot_managment.aiohttpSessionSetup import get_session
import asyncio
import time
import os

PRINT_PROGRESS = True
BATCH_PER_PRINT = 1000

# You can keep these but they are mostly unnecessary now
RATE_WINDOW = 70
MAX_REQUESTS = 10

GOOGLE_URL = "https://script.google.com/macros/s/AKfycbwuK932F2tcie74Pnnb8UiFhdKyCvdI4bblt29ywFy_Z7b97iAHZ9g3RNTNO-i4ow/exec"
GOOGLE_SECRET = os.getenv("GOOGLE_SCRIPT_KEY")  # must match Apps Script secret

class RateManager:
  def __init__(self, max_requests: int, window_seconds: int):
    self.max_requests = max_requests
    self.remaining = max_requests
    self.window_seconds = window_seconds
    self.reset_time = None
    self.lock = asyncio.Lock()

  async def acquire(self):
    while True:
      async with self.lock:
        now = time.time()

        if self.reset_time is not None and now >= self.reset_time:
          self.remaining = self.max_requests
          self.reset_time = None
          print("🔄 Rate window reset!")

        if self.remaining > 0:
          if self.reset_time is None:
            self.reset_time = now + self.window_seconds
          self.remaining -= 1
          return self.remaining

        sleep_time = (
          (self.reset_time - now)
          if self.reset_time is not None
          else self.window_seconds
        )

      if sleep_time > 0:
        print(f"⏳ Out of quota, waiting {sleep_time:.1f}s for reset...")
        await asyncio.sleep(max(sleep_time, 1))
      else:
        await asyncio.sleep(0.1)

RATE_MANAGER = RateManager(MAX_REQUESTS, RATE_WINDOW)


async def fetch_award_dates(user_id: str, badges: dict, sem, rate_mgr: RateManager) -> list[str]:
  dates = []
  badge_ids = list(badges.values())
  STEP = 100

  session = await get_session()

  async with sem:
    for i in range(0, len(badge_ids), STEP):
      chunk = badge_ids[i:i + STEP]

      params = {
        "userId": user_id,
        "badgeIds": ",".join(str(x) for x in chunk),
        "key": GOOGLE_SECRET,
      }

      # Rate manager mostly unnecessary now but kept for safety
      remaining = await rate_mgr.acquire()
      print(f"User {user_id}: {remaining} requests remaining this window")

      try:
        async with session.get(GOOGLE_URL, params=params) as response:

          if response.status != 200:
            print(f"Google relay HTTP {response.status} for user {user_id}")
            await asyncio.sleep(2)
            continue

          data = await response.json()

          # If relay returns error object
          if isinstance(data, dict) and data.get("error"):
            print(f"Relay error for {user_id}: {data}")
            await asyncio.sleep(2)
            continue

          for badge in data.get("data", []):
            if "awardedDate" in badge:
              dates.append(badge["awardedDate"])

          if PRINT_PROGRESS and len(dates) % BATCH_PER_PRINT == 0:
            print(f"{len(dates)} awarded dates for {user_id} requested.")

          # small delay just to be polite
          await asyncio.sleep(0.3)

      except Exception as e:
        print(f"Exception fetching award dates for {user_id}: {e}")
        await asyncio.sleep(2)
        continue

  return dates


async def fetch_multiple_award_dates(user_badges: list[dict], limit=5):
  sem = asyncio.Semaphore(limit)
  rate_mgr = RATE_MANAGER

  tasks = [
    fetch_award_dates(user_data["user_id"], user_data["badges"], sem, rate_mgr)
    for user_data in user_badges
    if user_data.get("badges")
  ]

  results = await asyncio.gather(*tasks)
  return results