from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

try:
    with engine.connect() as conn:
        print("✅ Connected to MySQL Database Successfully!")
except OperationalError as e:
    print("❌ Could not connect to MySQL Database:", e)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
