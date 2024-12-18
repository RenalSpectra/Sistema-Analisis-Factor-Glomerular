import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
SECRET_KEY = os.getenv("SECRET_KEY")
ADMIN = os.getenv("ADMIN_MAIL")
PASSWORD = os.getenv("PASSWORD")
allowed_origins = os.getenv('ALLOWED_ORIGINS', '').split(',')

