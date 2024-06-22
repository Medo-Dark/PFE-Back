import shutil
from typing import List
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
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
        def create_item(item: schemas.ItemBase, db: Session = Depends(get_db)):
            print("==========================")
            db_item = models.Item(name=item.name)
            db.add(db_item)
            db.commit()
            db.refresh(db_item)
            return db_item

        @self.router.get('/items/', response_model=List[schemas.Item])
        def get_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
            items = db.query(Item).offset(skip).limit(limit).all()
            return items

        @self.router.get('/items/{item_id}', response_model=schemas.Item)
        def get_item(item_id: int, db: Session = Depends(get_db)):
            db_item = db.query(Item).filter(Item.id == item_id).first()
            if not db_item:
                raise HTTPException(status_code=404, detail="Item not found")

            # Eager load the supplier items
            db_supplier_items = db.query(models.SupplierItem).filter(models.SupplierItem.item_id == item_id).all()
            db_item.supplier_items = db_supplier_items

            return db_item
        @self.router.get('/itemsRequest/{item_id}', response_model=schemas.ItemRequests)
        def get_item(item_id: int, db: Session = Depends(get_db)):
            db_item = db.query(Item).filter(Item.id == item_id).first()
            if not db_item:
                raise HTTPException(status_code=404, detail="Item not found")

            # Eager load the supplier items
            db_Request_items = db.query(models.RequestItem).filter(models.RequestItem.item_id == item_id).all()
            print(db_Request_items,"----------------------")
            db_item.requests = db_Request_items

            return db_item
        
        @self.router.post('/items/upload')
        def upload_file(uploaded_file: UploadFile = File(...)):
            path = f"files/{uploaded_file.filename}"
            with open(path, 'w+b') as file:
                shutil.copyfileobj(uploaded_file.file, file)

            return {
                'file': uploaded_file.filename,
                'content': uploaded_file.content_type,
                'path': path,
            }
        

router = ItemRouter(item_repository, schemas.Item).router
