from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os

DATABASE_URL = os.getenv('DATABASE_URL')
print(DATABASE_URL)

#DATABASE_URL = f"postgresql://bootcamp_user:admin@{DB_IP}:5432/bootcamp_db"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()