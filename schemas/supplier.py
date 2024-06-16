from typing import List, Optional
from pydantic import BaseModel

class SupplierBase(BaseModel):
    name: str
    contact_info: str = None


class SupplierCreate(SupplierBase):
    pass

class SupplierItem(SupplierBase):
    id: int
    
    class Config:
        from_attributes = True

class Supplier(SupplierBase):
    id: int
    # items2: List['Item']
    
    class Config:
        from_attributes = True

# from .item import Item
