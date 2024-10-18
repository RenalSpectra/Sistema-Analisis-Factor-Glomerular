from config import supabase



session = supabase.auth.get_session()
print(session)

response = supabase.auth.sign_in_with_password({'email':'renalspectra@gmail.com', 'password':'rSP3CTR@'})
session = supabase.auth.get_session()
print(session)


response = supabase.auth.sign_out()
