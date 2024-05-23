from config.settings import get_settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DB_QRM_URL = get_settings().DB_URL
DB_DATA_QRM_URL = get_settings().DB_DATA_URL

engine = create_engine(DB_QRM_URL)
engine_data = create_engine(DB_DATA_QRM_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocalData = sessionmaker(autocommit=False, autoflush=False, bind=engine_data)

Base = declarative_base()
Base_Data = declarative_base()
