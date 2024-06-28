# app/schemas/supplier.py
from pydantic import BaseModel
from typing import List, Optional

class ItemBase(BaseModel):
    part_number: str
    isDrg :bool
    image : Optional[str] = None
    DwgTitle  :str
    DWG_REV :str

    class Config:
        from_attributes = True

class SupplierItemBase(BaseModel):
    price: int

class SupplierItemCreate(SupplierItemBase):
    item_id: int


class SupplierItemOut(SupplierItemBase):
    item: ItemBase

    class Config:
        from_attributes = True

class SupplierBase(BaseModel):
    name: str
    contact_info: str


class SupplierCreate(SupplierBase):
    pass

class SupplierOut(SupplierBase):
    id: int
    supplier_items: List[SupplierItemOut] = None

    class Config:
        from_attributes = True
