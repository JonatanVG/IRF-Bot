from bot_managment.supabase_setup import Supabase, Supabase2
import requests
import time
from supabase_auth import datetime

def keep_alive(KOYEB_URL):
    while True:
        try:
            r = requests.get(KOYEB_URL, timeout=30)
            print(f"Keep-alive ping successful: {r.status_code}")
            print("Auditing bot start/restart in audit_log table.")
            Supabase.table('audit_log').insert({'reason': 'Bot Started/Restarted', 'removal_date': str(datetime.now().strftime('%H:%M-%d.%m.%Y')), 'removed_item': 'N/A', 'category': 'Bot Event'}).execute()
            print("Bot start/restart logged successfully.")
            print("Auditing bot start/restart in second audit_log table.")
            Supabase2.table("audit_log").insert({"category": "Bot started", "removal_date": f"{str(datetime.now().strftime('%H:%M-%d.%m.%Y'))}", "removed_item": "N/A", "reason": "Bot started"}).execute()
            print("Bot start/restart logged successfully in second table.")
        except requests.exceptions.RequestException as e:
            print(f"Keep-alive ping failed: {e}")
        time.sleep(1800)  # Ping every 30 minutes