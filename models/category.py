from config.database import Base_Data
from sqlalchemy import Column, Integer, String, Text

class Category(Base_Data):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(255))
    code = Column(Integer)
    category = Column(Text)
    sub_category = Column(Text)