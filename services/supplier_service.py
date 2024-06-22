from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.dependencies import get_db

import models.supplier as models
import schemas.supplier as schemas
from repositories.request_repo import SupplierRepository
from services.base_service import BaseRouter
import models.item as ItemModel




supp_repository = SupplierRepository()


router = APIRouter(prefix='/Supplier', tags=['Supplier'])

class SupplierRouter(BaseRouter[models.Supplier, schemas.SupplierOut]):
    def __init__(self, repository, responseType):
        super().__init__(responseType=responseType, repository=repository)

        @self.router.post('/suppliers/', response_model=schemas.SupplierOut)
        def create_supplier(supplier: schemas.SupplierCreate, db: Session = Depends(get_db)):
            db_supplier = models.Supplier(name=supplier.name, contact_info=supplier.contact_info)
            db.add(db_supplier)
            db.commit()
            db.refresh(db_supplier)
            return db_supplier
        @self.router.post('/suppliers/{supplier_id}/items/', response_model=schemas.SupplierItemOut)
        def add_item_to_supplier(supplier_id: int, supplier_item: schemas.SupplierItemCreate, db: Session = Depends(get_db)):
            db_supplier = db.query(models.Supplier).filter(models.Supplier.id == supplier_id).first()
            if not db_supplier:
                raise HTTPException(status_code=404, detail="Supplier not found")

            db_item = db.query(ItemModel.Item).filter(ItemModel.Item.id == supplier_item.item_id).first()
            if not db_item:
                raise HTTPException(status_code=404, detail="Item not found")

            db_supplier_item = ItemModel.SupplierItem(
                supplier_id=supplier_id,
                item_id=supplier_item.item_id,
                price=supplier_item.price
            )
            db.add(db_supplier_item)
            db.commit()
            db.refresh(db_supplier_item)
            return db_supplier_item

        @self.router.get('/suppliers/{supplier_id}', response_model=schemas.SupplierOut)
        def get_supplier(supplier_id: int, db: Session = Depends(get_db)):
            db_supplier = db.query(models.Supplier).filter(models.Supplier.id == supplier_id).first()
            if not db_supplier:
                raise HTTPException(status_code=404, detail="Supplier not found")

            # Eager load the supplier items
            db_supplier_items = db.query(ItemModel.SupplierItem).filter(ItemModel.SupplierItem.supplier_id == supplier_id).all()
            print("-------------------------------------",db_supplier_items)
            db_supplier.supplier_items = db_supplier_items
            
            return db_supplier

router = SupplierRouter(supp_repository, schemas.SupplierOut).router
