# app/schemas/item.py
from pydantic import BaseModel
from typing import List, Optional

from .supplier import SupplierBase

class SupplierItemBase(BaseModel):
    price: int
    supplier_id: int


class RequestItemBase(BaseModel):
    item_id: int
    request_id: int
    quantity: int
    Purchase_state:bool = False


class RequestItemOut(RequestItemBase):
    pass

class SupplierItemOut(SupplierItemBase):
    supplier: SupplierBase

    class Config:
        from_attributes = True


class ItemBase(BaseModel):
    name: str

class ItemCreate(ItemBase):
    quantity: int

class Item(ItemBase):
    id: int
    supplier_items: List[SupplierItemOut] = None

    class Config:
        from_attributes = True


class ItemRequests(ItemBase):
    id: int
    requests: List[RequestItemOut] = None

    class Config:
        from_attributes = True
    

  






