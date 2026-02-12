import aiohttp
import os

SESSION = None

async def get_session():
  global SESSION

  if SESSION is None or SESSION.closed:
    roblox_cookie = os.getenv("ROBLOX_COOKIE")

    headers = {
      "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/120 Safari/537.36"
      ),
      "Accept": "application/json",
      "Connection": "keep-alive",
    }

    # Add cookie if present
    if roblox_cookie:
      headers["Cookie"] = f".ROBLOSECURITY={roblox_cookie}"

    connector = aiohttp.TCPConnector(
      limit=20,
      ttl_dns_cache=300,
      ssl=False
    )

    SESSION = aiohttp.ClientSession(
      headers=headers,
      connector=connector,
      timeout=aiohttp.ClientTimeout(total=30),
      trust_env=True
    )

  return SESSION


async def close_session():
  global SESSION
  if SESSION and not SESSION.closed:
    await SESSION.close()