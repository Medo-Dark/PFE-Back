# app/schemas/purchase.py
from pydantic import BaseModel
from typing import List

class PurchaseItemBase(BaseModel):
    item_id: int
    quantity: int
    price: int

class PurchaseItemCreate(PurchaseItemBase):
    pass
class PurchaseItemOut(PurchaseItemBase):
    purchase_id: int

    class Config:
        from_attributes = True

class PurchaseBase(BaseModel):
    supplier_id: int
    buyer_id: int

class PurchaseCreate(PurchaseBase):
    request_id:int
    items: List[PurchaseItemCreate]


class AddItemsToPurchase(BaseModel):
    request_id:int
    items: List[PurchaseItemCreate]

class PurchaseOut(PurchaseBase):
    id: int
    purchase_items: List[PurchaseItemOut]

    class Config:
        from_attributes = True
