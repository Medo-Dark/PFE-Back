# app/schemas/item.py
from fastapi import UploadFile
from pydantic import BaseModel
from typing import List, Optional

from .supplier import SupplierBase

class SupplierItemBase(BaseModel):
    price: int = None
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

class SupplierItemPurch(SupplierItemBase):
    supplier: SupplierBase
    purchasing:bool

    class Config:
        from_attributes = True


class ItemBase(BaseModel):
    part_number: str
    isDrg :bool = False
    image : Optional[str] = None
    DwgTitle  :str
    DWG_REV :str

class ItemCreate(ItemBase):
    quantity: int

class Item(ItemBase):
    id: int
    supplier_items: List[SupplierItemOut] = None

    class Config:
        from_attributes = True

class ItemOut(ItemBase):
    id: int
    quantity:int = 0 

    class Config:
        from_attributes = True

class ItemPurch(ItemBase):
    id: int
    supplier_items: List[SupplierItemPurch] = None

    class Config:
        from_attributes = True


class ItemRequests(ItemBase):
    id: int
    requests: List[RequestItemOut] = None

    class Config:
        from_attributes = True
    

  






