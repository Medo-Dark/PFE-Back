from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.dependencies import get_db

import models.supplier as models
import schemas.supplier as schemas
from repositories.request_repo import SupplierRepository
from services.base_service import BaseRouter




supp_repository = SupplierRepository()


router = APIRouter(prefix='/Supplier', tags=['Supplier'])

class SupplierRouter(BaseRouter[models.Supplier, schemas.Supplier]):
    def __init__(self, repository, responseType):
        super().__init__(responseType=responseType, repository=repository)

        @self.router.post('/suppliers/', response_model=schemas.Supplier)
        def create_supplier(supplier: schemas.SupplierCreate, db: Session = Depends(get_db)):
            print("-------------ALO----------",supplier)
            db_supplier = models.Supplier(name=supplier.name,
            contact_info= supplier.contact_info   
              )
            print("-------------ALO2----------")
            
            db.add(db_supplier)
            db.commit()
            db.refresh(db_supplier)
            return db_supplier

        # @self.router.get('/suppliers/', response_model=list[Supplier])
        # def get_suppliers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
        #     suppliers = db.query(Supplier).offset(skip).limit(limit).all()
        #     return suppliers

        # @self.router.get('/suppliers/{supplier_id}', response_model=Supplier)
        # def get_supplier(supplier_id: int, db: Session = Depends(get_db)):
        #     supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
        #     if supplier is None:
        #         raise HTTPException(status_code=404, detail='Supplier not found')
        #     return supplier

router = SupplierRouter(supp_repository, schemas.Supplier).router
