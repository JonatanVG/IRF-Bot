import os
import aiohttp

koyeb_api = os.getenv("KOYEB_API") # Write this to access your Koyeb API key.
service_id = os.getenv("KOYEB_SERVICE_ID") # Write this to access your Koyeb service ID.

async def stop_koyeb_service():
  url = f"https://api.koyeb.com/v1/services/{service_id}/stop"
  headers = {
      "Authorization": f"Bearer {koyeb_api}",
      "Content-Type": "application/json"
  }

  payload = {
    "definition": {
      "instance_types": [],
      "scaling": {
        "min": 0,
        "max": 0
      }
    }
  }

  async with aiohttp.ClientSession() as session:
      async with session.patch(url, json=payload, headers=headers) as response:
          return await response.text()