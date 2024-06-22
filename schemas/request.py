# app/schemas/request.py
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
    title:str
    description: str
    status: Optional[StatusEnum]="Pending"
    buyer_id: int 





class RequestCreate(RequestBase):
    title: str
    description: str
    items: List[ItemCreate]

class Request(RequestBase):
    id: int
    requestor_id: int
    request_items: list[RequestItemOut]

    

    class Config:
        from_attributes  = True
