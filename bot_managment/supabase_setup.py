import os
import supabase

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
Supabase = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

SUPABASE2_URL = os.getenv("SUPABASE2_URL")
SUPABASE2_KEY = os.getenv("SUPABASE2_KEY")
Supabase2 = supabase.create_client(SUPABASE2_URL, SUPABASE2_KEY)