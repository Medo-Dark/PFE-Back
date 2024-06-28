# app/schemas/request.py
from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from typing import List, Optional, Union


from .item import ItemCreate , Item


class StatusEnum(str, Enum):
    PENDING = 'Pending'
    ACCEPTED = 'Accepted'
    REJECTED = 'Rejected'
    COMPLETED = 'Completed'


class RequestItemBase(BaseModel):
    item_id: int
    request_id: int
    quantity: int
    Purchase_state:bool = False

class RequestItemOut(BaseModel):
    quantity: int
    Purchase_state:bool = False
    item : Item



class RequestBase(BaseModel):
    remark: bool
    delivery_date : datetime
    demand_PCS_not_DWG_related:int
    departement:str
    plant:str
    storageLocation:str
    status: Optional[StatusEnum]="Pending"
    buyer_id: int 



class UserBase(BaseModel):
    username: str
    email: str


class RequestCreate(RequestBase):
    items: List[ItemCreate]

class QuickItem(BaseModel):
    item_id:int
    quantity:int

class QuickRequestCreate(RequestBase):
    items: List[QuickItem]


class Request(RequestBase):
    id: int
    inflowDate:datetime
    requestor_id: int
    requestor:UserBase
    request_items: list[RequestItemOut]

    class Config:
        from_attributes  = True


class RequestorRequest(RequestBase):
    id: int
    inflowDate:datetime
    requestor_id: int
    buyer:UserBase

    

    class Config:
        from_attributes  = True
