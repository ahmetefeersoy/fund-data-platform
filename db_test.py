from sqlalchemy import create_engine

uri = "postgresql://postgres:AHMETefe0303@db.ewrwjgenruaegkbhbnok.supabase.co:5432/postgres"

try:
    engine = create_engine(uri)
    conn = engine.connect()
    print("CONNECTED OK")
except Exception as e:
    print("ERROR:", e)
