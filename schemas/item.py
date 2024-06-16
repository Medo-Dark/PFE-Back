# app/schemas/item.py
from pydantic import BaseModel

class ItemBase(BaseModel):
    name: str
    quantity: int

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True
    

    






