from config.database import Base_Data
from sqlalchemy import Column, Integer, String, Text

class Cause(Base_Data):
    __tablename__ = 'causes'
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(255))
    cause_number = Column(Integer)
    cause = Column(Text)
    sub_cause_number = Column(Integer)
    sub_cause = Column(Text)