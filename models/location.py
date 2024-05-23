from config.database import Base_Data
from sqlalchemy import Column, Integer, String


class Location(Base_Data):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True, index=True)
    plant = Column(String(50))
    project = Column(String(50))
    area = Column(String(50))
    line = Column(String(50))
