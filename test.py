from config import supabase



response = supabase.auth.sign_out()
