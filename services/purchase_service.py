# app/routers/purchases.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.purchase import Purchase
from models.purchase import PurchaseItem
from models.supplier import Supplier
from models.item import Item
from models.user import User
from schemas.purchase import PurchaseCreate, PurchaseOut
from config.dependencies import get_db
from models.item import RequestItem


import models.purchase as models
import schemas.purchase as schemas
from repositories.request_repo import PurchaseRepository
from services.base_service import BaseRouter





purchase_repository = PurchaseRepository()


router = APIRouter(prefix='/Purchase', tags=['Purchase'])

class ItemRouter(BaseRouter[models.Purchase, schemas.PurchaseOut]):
    def __init__(self, repository, responseType):
        super().__init__(responseType=responseType, repository=repository)

        @self.router.post('/purchases/', response_model=PurchaseOut)
        def create_purchase(purchase: PurchaseCreate, db: Session = Depends(get_db)):
            db_supplier = db.query(Supplier).filter(Supplier.id == purchase.supplier_id).first()
            if not db_supplier:
                raise HTTPException(status_code=404, detail="Supplier not found")

            db_buyer = db.query(User).filter(User.id == purchase.buyer_id, User.role == 'Buyer').first()
            if not db_buyer:
                raise HTTPException(status_code=404, detail="Buyer not found")


            db_purchase = Purchase(supplier_id=purchase.supplier_id, buyer_id=purchase.buyer_id)
            db.add(db_purchase)
            db.commit()
            db.refresh(db_purchase)

            for item in purchase.items:
                db_item = db.query(Item).filter(Item.id == item.item_id).first()
                if not db_item:
                    raise HTTPException(status_code=404, detail=f"Item with ID {item.item_id} not found")

                db_requestItem = db.query(RequestItem).filter(RequestItem.request_id  ==  purchase.request_id ,RequestItem.item_id == item.item_id ).first()
                
                if not db_requestItem:
                    raise HTTPException(status_code=404, detail="Request not found")
                
                db_requestItem.Purchase_state=True

                db_purchase_item = PurchaseItem(
                    purchase_id=db_purchase.id,
                    item_id=item.item_id,
                    quantity=item.quantity,
                    price=item.price
                )
                db.add(db_purchase_item)
            
            db.commit()
            db.refresh(db_purchase)

            return db_purchase

        @self.router.get('/purchases/{purchase_id}', response_model=PurchaseOut)
        def get_purchase(purchase_id: int, db: Session = Depends(get_db)):
            db_purchase = db.query(Purchase).filter(Purchase.id == purchase_id).first()
            if not db_purchase:
                raise HTTPException(status_code=404, detail="Purchase not found")

            return db_purchase

        @self.router.get('/buyers/{buyer_id}/purchases/', response_model=List[PurchaseOut])
        def get_purchases_by_buyer(buyer_id: int, db: Session = Depends(get_db)):
            db_buyer = db.query(User).filter(User.id == buyer_id, User.role == 'Buyer').first()
            if not db_buyer:
                raise HTTPException(status_code=404, detail="Buyer not found")

            return db_buyer.purchases
        
        @self.router.post('/purchases/{purchase_id}/add-items', response_model=PurchaseOut)
        def add_items_to_purchase(purchase_id: int, items: schemas.AddItemsToPurchase, db: Session = Depends(get_db)):
            db_purchase = db.query(Purchase).filter(Purchase.id == purchase_id).first()
            if not db_purchase:
                raise HTTPException(status_code=404, detail="Purchase not found")

            for item in items.items:
                db_item = db.query(Item).filter(Item.id == item.item_id).first()
                if not db_item:
                    raise HTTPException(status_code=404, detail=f"Item with ID {item.item_id} not found")

                db_requestItem = db.query(RequestItem).filter(RequestItem.request_id  ==  items.request_id ,RequestItem.item_id == item.item_id ).first()
                
                if not db_requestItem:
                    raise HTTPException(status_code=404, detail="Request not found")
                
                db_requestItem.Purchase_state=True
                
                
                db_purchase_item = PurchaseItem(
                    purchase_id=db_purchase.id,
                    item_id=item.item_id,
                    quantity=item.quantity,
                    price=item.price
                )
                db.add(db_purchase_item)

            db.commit()
            db.refresh(db_purchase)

            return db_purchase
        


router = ItemRouter(purchase_repository, schemas.PurchaseOut).router
