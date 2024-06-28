import shutil
from typing import List, Optional
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from models.item import Item
from config.dependencies import get_db 
from auth.dependencies import  upload_File
from models.supplier import Supplier
from models.purchase import Purchase
from sqlalchemy.exc import SQLAlchemyError
from consts import static_exceptions as exceptions

import models.item as models
import schemas.item as schemas
from repositories.request_repo import ItemRepository
from services.base_service import BaseRouter
from models.request import Request



item_repository = ItemRepository()


router = APIRouter(prefix='/Items', tags=['Items'])

class ItemRouter(BaseRouter[models.Item, schemas.Item]):
    def __init__(self, repository, responseType):
        super().__init__(responseType=responseType, repository=repository)

        @self.router.post('/items/', response_model=schemas.Item)
        def create_item(item: schemas.ItemBase, db: Session = Depends(get_db)):
            print("==========================")
            try:
                
                db_item = Item(
                            part_number= item.part_number,
                            isDrg = item.isDrg,
                            DwgTitle= item.DwgTitle,
                            DWG_REV= item.DWG_REV

                        )
                if item.image :
                    file = upload_File(item.image)
                    db_item.image = file.path

                db.add(db_item)
                db.commit()
                db.refresh(db_item)

            except SQLAlchemyError:
                db.rollback()
                raise exceptions.transaction_failed
            else:
                db.commit()
                return db_item


        @self.router.get('/items/', response_model=List[schemas.Item])
        def get_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
            items = db.query(Item).offset(skip).limit(limit).all()
            return items

        @self.router.get('/itemsOut/', response_model=List[schemas.ItemOut])
        def get_items_with_q(db: Session = Depends(get_db)):
            items = db.query(Item).all()
            return items

        @self.router.get('/items/{item_id}/buyer/{buyer_id}', response_model=schemas.ItemPurch)
        def get_item(item_id: int,buyer_id:int, db: Session = Depends(get_db)):
            db_item = db.query(Item).filter(Item.id == item_id).first()
            if not db_item:
                raise HTTPException(status_code=404, detail="Item not found")

            # Eager load the supplier items
            db_supplier_items = db.query(models.SupplierItem).filter(models.SupplierItem.item_id == item_id).all()
            for supplier in db_supplier_items :
                purchases = db.query(Purchase).filter(Purchase.buyer_id == buyer_id  ,Purchase.supplier_id == supplier.supplier_id,Purchase.done==False).all()
                print("323424234")
                if(purchases):
                    supplier.purchasing = True
                else:
                    supplier.purchasing = False
                    print(supplier.purchasing)
            db_item.supplier_items = db_supplier_items

            return db_item
        @self.router.get('/itemsRequest/{item_id}', response_model=schemas.ItemRequests)
        def get_item_requests(item_id: int, db: Session = Depends(get_db)):
            db_item = db.query(Item).filter(Item.id == item_id).first()
            if not db_item:
                raise HTTPException(status_code=404, detail="Item not found")

            # Eager load the supplier items
            db_Request_items = db.query(models.RequestItem).filter(models.RequestItem.item_id == item_id).all()
            print(db_Request_items,"----------------------")
            db_item.requests = db_Request_items

            return db_item
        @self.router.get('/itemsRequestPurch/{item_id}/Buyer/{buyer_id}', response_model=schemas.ItemRequests)
        def get_Unpurchased_item_requests(item_id: int,buyer_id:int, db: Session = Depends(get_db)):
            db_item = db.query(Item).filter(Item.id == item_id).first()
            if not db_item:
                raise HTTPException(status_code=404, detail="Item not found")

            db_Request_items = db.query(models.RequestItem).join(Request).filter(models.RequestItem.item_id == item_id , models.RequestItem.Purchase_state == False , Request.buyer_id == buyer_id).all()
            print(db_Request_items,"----------------------")
            db_item.requests = db_Request_items

            return db_item
        
        @self.router.post('/items/upload/{item_id}')
        def upload_file( item_id: int, db: Session = Depends(get_db) , uploaded_file: UploadFile = File(...) ):
            db_item = db.query(Item).filter(Item.id == item_id).first()
            if not db_item:
                raise HTTPException(status_code=404, detail="Item not found")

            path = f"files/{uploaded_file.filename}{item_id}"
            with open(path, 'w+b') as file:
                shutil.copyfileobj(uploaded_file.file, file)
            db_item.image = path
            db_item.isDrg = True
            try:
                db.commit()
            except: 
                raise HTTPException(status_code=404, detail="Cannot update record")

                        
            return {
                'file': uploaded_file.filename,
                'content': uploaded_file.content_type,
                'path': path,
            }
        

router = ItemRouter(item_repository, schemas.Item).router
