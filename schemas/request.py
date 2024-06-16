# app/schemas/request.py
from enum import Enum
from pydantic import BaseModel
from typing import List, Optional
from .item import ItemCreate , Item


class StatusEnum(str, Enum):
    PENDING = 'Pending'
    ACCEPTED = 'Accepted'
    REJECTED = 'Rejected'
    COMPLETED = 'Completed'


class RequestBase(BaseModel):
    title:str
    description: str
    status: Optional[StatusEnum]="Pending"




class RequestCreate(RequestBase):
    buyer_id:int
    items: list[ItemCreate]


class Request(RequestBase):
    id: int
    requestor_id: int
    buyer_id: int 
    items: list[Item]

    

    class Config:
        from_attributes  = True
