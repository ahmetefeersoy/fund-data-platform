import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv()


database_url = os.environ.get("DATABASE_URL")
if not database_url:
    raise RuntimeError("DATABASE_URL environment variable is not set")

engine = create_engine(database_url)
