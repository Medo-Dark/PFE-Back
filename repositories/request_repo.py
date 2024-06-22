
from typing import List
from sqlalchemy import or_
from sqlalchemy.orm import Session

from repositories.crud_repo import CRUDRepository
from models.request import  Request
from models.item import  Item
from models.supplier import  Supplier
from models.purchase import  Purchase



class RequestRepository(CRUDRepository):
    def __init__(self) -> None:
        super().__init__(Request)


class ItemRepository(CRUDRepository):
    def __init__(self) -> None:
        super().__init__(Item)


class SupplierRepository(CRUDRepository):
    def __init__(self) -> None:
        super().__init__(Supplier)


class PurchaseRepository(CRUDRepository):
    def __init__(self) -> None:
        super().__init__(Purchase)

