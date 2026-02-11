from bot_managment.supabase_setup import Supabase
def user_authorized(user_id: int):
  # Check if the user is in the database
  response = (
    Supabase
    .table("AUTHORIZED_BOT_USERS")
    .select("*")
    .eq("USER_ID", user_id)
    .execute()
  )
  return bool(response.data)  # Return True if the user is in the database, False otherwise