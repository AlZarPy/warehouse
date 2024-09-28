import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

PGUSER = os.environ["PGUSER"]
PGPASSWORD = os.environ["PGPASSWORD"]
PGDATABASE = os.environ["PGDATABASE"]

DATABASE_URL = f"postgresql://{PGUSER}:{PGPASSWORD}@db:5432/{PGDATABASE}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
