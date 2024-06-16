from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.item import Item
from config.dependencies import get_db
from models.supplier import Supplier

import models.item as models
import schemas.item as schemas
from repositories.request_repo import ItemRepository
from services.base_service import BaseRouter



item_repository = ItemRepository()


router = APIRouter(prefix='/Items', tags=['Items'])

class ItemRouter(BaseRouter[models.Item, schemas.Item]):
    def __init__(self, repository, responseType):
        super().__init__(responseType=responseType, repository=repository)

        @self.router.post('/items/', response_model=schemas.Item)
        def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
            db_item = models.Item(name=item.name,
            description=item.description,
            request_id= item.request_id
                                  )
            # suppliers = db.query(Supplier).filter(Supplier.id.in_(item.supplier_ids)).all()
            # if not suppliers or len(suppliers) != len(item.supplier_ids):
            #     raise HTTPException(status_code=404, detail='One or more suppliers not found')

            # db_item.suppliers.extend(suppliers)
            db.add(db_item)
            db.commit()
            db.refresh(db_item)
            return db_item

        @self.router.get('/items/', response_model=List[schemas.Item])
        def get_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
            items = db.query(Item).offset(skip).limit(limit).all()
            return items


router = ItemRouter(item_repository, schemas.Item).router
