from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from databases import Database
from dotenv import load_dotenv

import os

# Environment variables
load_dotenv('./.env')
user = os.environ.get("POSTGRES_USER")
password = os.environ.get("POSTGRES_PASSWORD")
database_name = os.environ.get("POSTGRES_DB")
port = os.environ.get("POSTGRES_PORT")

# Database configuration
DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@{port}/{database_name}"
database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
