from bot_managment.supabase_setup import Supabase

KOYEB_URL = ""

def load_koyeb_url():
  global KOYEB_URL
  try:
    KOYEB_URL = Supabase.table("KOYEB_URL").select("KOYEB_URL").execute().data[0]["KOYEB_URL"]
    print(f"Koyeb URL loaded successfully: {KOYEB_URL}")
    return KOYEB_URL
  except Exception as e:
    print(f"Failed to load Koyeb URL: {e}")