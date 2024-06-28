from datetime import datetime, timezone
from typing import List

from fastapi import Depends ,APIRouter, HTTPException
from sqlalchemy.orm import Session

import models.request as models
from schemas.item import ItemBase
import schemas.request as schemas
from config.dependencies import get_db
from consts.custom_exceptions import CustomHTTPException
from repositories.request_repo import RequestRepository , ItemRepository

from auth.authentication import get_current_user
from schemas.response import Response
import models.user as modelsUser
from sqlalchemy.exc import SQLAlchemyError
from services.base_service import BaseRouter
from models.item import Item, RequestItem 
from schemas.user import User

req_repository = RequestRepository()
item_repo = ItemRepository()

router = APIRouter(prefix='/Requests', tags=['Requests'])

class RequestRouter(BaseRouter[models.Request, schemas.Request]):
    def __init__(self, repository, responseType):
        super().__init__(responseType=responseType, repository=repository)

        @self.router.post('/CreateReq', response_model=schemas.Request)
        def create_request(request: schemas.RequestCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
            try:
                if current_user.role != 'Requestor':
                    raise HTTPException(status_code=403, detail='Only requestors can create requests')
                
                

                buyer = db.query(modelsUser.User).filter( modelsUser.User.id == request.buyer_id, modelsUser.User.role.in_(['Buyer', 'Admin']) ).first()

                if not buyer:
                    raise HTTPException(status_code=404, detail='Buyer not found')
                
                if request.delivery_date <= datetime.now(timezone.utc):
                    raise HTTPException(status_code=404, detail='Delivery date should be above the current time')

              
                db_request = models.Request(
                        requestor_id = current_user.id,
                        remark=request.remark,
                        delivery_date=request.delivery_date,
                        demand_PCS_not_DWG_related=request.demand_PCS_not_DWG_related,
                        departement=request.departement,
                        plant=request.plant,
                        storageLocation=request.storageLocation,
                        status=request.status,
                        buyer_id=request.buyer_id
                    )

                print("-----------HALO-------------------------",db_request.remark)
                db.add(db_request)
                db.commit()
                db.refresh(db_request)

               
                print("-----------HALO2-------------------------")

                # Add items to the request
                # Handle items
                for item in request.items:
                    # Check if the item already exists
                    db_item = db.query(Item).filter(Item.part_number == item.part_number).first()
                    if not db_item:
                        # Create a new item if it doesn't exist
                        
                        db_item = Item(
                            part_number= item.part_number,
                            isDrg = item.isDrg,
                            image= item.image,
                            DwgTitle= item.DwgTitle,
                            DWG_REV= item.DWG_REV

                        )
                        db.add(db_item)
                        db.commit()
                        db.refresh(db_item)

                    # Link the item to the request with quantity
                    db_request_item = RequestItem(
                        request_id=db_request.id,
                        item_id=db_item.id,
                        quantity=item.quantity
                    )
                    db.add(db_request_item)

                print('-----------------------1------------------------------')
                db.commit()                
                print('-----------------------2------------------------------')
                
                return db_request
            except SQLAlchemyError as e:
                db.rollback()
                return {"error": str(e)}

        @self.router.post('/CreateQuickReq', response_model=schemas.Request)
        def create_quick_request(request: schemas.QuickRequestCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
            try:
                if current_user.role != 'Requestor':
                    raise HTTPException(status_code=403, detail='Only requestors can create requests')
                
                

                buyer = db.query(modelsUser.User).filter( modelsUser.User.id == request.buyer_id, modelsUser.User.role.in_(['Buyer', 'Admin']) ).first()

                if not buyer:
                    raise HTTPException(status_code=404, detail='Buyer not found')
                
                if request.delivery_date <= datetime.now(timezone.utc):
                    raise HTTPException(status_code=404, detail='Delivery date should be above the current time')

              
                db_request = models.Request(
                        requestor_id = current_user.id,
                        remark=request.remark,
                        delivery_date=request.delivery_date,
                        demand_PCS_not_DWG_related=request.demand_PCS_not_DWG_related,
                        departement=request.departement,
                        plant=request.plant,
                        storageLocation=request.storageLocation,
                        status=request.status,
                        buyer_id=request.buyer_id
                    )

                print("-----------HALO-------------------------",db_request.remark)
                db.add(db_request)
                db.commit()
                db.refresh(db_request)

               
                print("-----------HALO2-------------------------")

                # Add items to the request
                # Handle items
                for item in request.items:
                    # Check if the item already exists
                    db_item = db.query(Item).filter(Item.id == item.item_id).first()
                    
                    # Link the item to the request with quantity
                    db_request_item = RequestItem(
                        request_id=db_request.id,
                        item_id=db_item.id,
                        quantity=item.quantity
                    )
                    db.add(db_request_item)

                print('-----------------------1------------------------------')
                db.commit()                
                print('-----------------------2------------------------------')
                
                return db_request
            except SQLAlchemyError as e:
                db.rollback()
                return {"error": str(e)}


        @self.router.get('/buyers/{buyer_id}/requests/', response_model=List[schemas.Request])
        def get_requests_by_buyer(buyer_id: int, db: Session = Depends(get_db)):
            db_buyer = db.query(modelsUser.User).filter(modelsUser.User.id == buyer_id, modelsUser.User.role.in_(['Buyer', 'Admin'])).first()
            if not db_buyer:
                raise HTTPException(status_code=404, detail="Buyer not found")

            return db_buyer.requests_received

        @self.router.get('/requestor/{requestor_id}/requests/', response_model=List[schemas.RequestorRequest])
        def get_requestor_request(requestor_id: int, db: Session = Depends(get_db)):
            db_requestor = db.query(modelsUser.User).filter(modelsUser.User.id == requestor_id, modelsUser.User.role == 'Requestor').first()
            if not db_requestor:
                raise HTTPException(status_code=404, detail="db_requestor not found")

            return db_requestor.requests_made

router = RequestRouter(req_repository, schemas.Request).router
