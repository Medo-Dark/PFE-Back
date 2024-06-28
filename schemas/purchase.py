# app/schemas/purchase.py
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class ItemBase(BaseModel):
    part_number: str
    isDrg :bool
    image : Optional[str] = None
    DwgTitle  :str
    DWG_REV :str

class SupplierBase(BaseModel):
    name: str
    contact_info: str

class PurchaseItemBase(BaseModel):
    item_id: int
    quantity: int
    price: int = 0
    



class PurchaseItemCreate(PurchaseItemBase):
    request_id:int

class PurchaseItemAdd(PurchaseItemBase):
    requests_ids:List[int]

class PurchaseItemOut(PurchaseItemBase):
    item:ItemBase
    purchase_id: int
    

class PurchaseBase(BaseModel):
    supplier_id: int
    buyer_id: int
    created_at:datetime = None
    done : bool = False

class PurchaseCreate(PurchaseBase):
    items: List[PurchaseItemCreate]

class PurchaseCreateOne(PurchaseBase):
    item: PurchaseItemAdd


class AddItemsToPurchase(BaseModel):
    items: List[PurchaseItemCreate]

class AddItemToPurchase(BaseModel):
    item: PurchaseItemAdd

class PurchaseOut(PurchaseBase):
    id: int
    created_at:datetime
    supplier:SupplierBase
    purchase_items: List[PurchaseItemOut]

    class Config:
        from_attributes = True

class PurchaseItemOutPurchase(PurchaseItemBase):
    item:ItemBase
    supplier:SupplierBase
    purchase_id: int
    purchase:PurchaseBase

    class Config:
        from_attributes = True
