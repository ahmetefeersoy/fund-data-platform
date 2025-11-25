from sqlalchemy import create_engine

import os
from dotenv import load_dotenv
load_dotenv()


database_url = os.environ.get("DATABASE_URL")

try:
    engine = create_engine(database_url)
    conn = engine.connect()
    print("CONNECTED OK")
except Exception as e:
    print("ERROR:", e)
