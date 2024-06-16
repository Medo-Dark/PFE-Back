from typing import List

from fastapi import Depends ,APIRouter, HTTPException
from sqlalchemy.orm import Session

import models.request as models
import schemas.request as schemas
from config.dependencies import get_db
from consts.custom_exceptions import CustomHTTPException
from repositories.request_repo import RequestRepository
from auth.authentication import get_current_user
from schemas.response import Response
import models.user as modelsUser
from sqlalchemy.exc import SQLAlchemyError
from services.base_service import BaseRouter
from models.item import Item
from schemas.user import User

req_repository = RequestRepository()

router = APIRouter(prefix='/Requests', tags=['Requests'])

class RequestRouter(BaseRouter[models.Request, schemas.Request]):
    def __init__(self, repository, responseType):
        super().__init__(responseType=responseType, repository=repository)

        @self.router.post('/CreateReq', response_model=schemas.Request)
        def create_request(request: schemas.RequestCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
            try:
                if current_user.role != 'Requestor':
                    raise HTTPException(status_code=403, detail='Only requestors can create requests')
                

                buyer = db.query(modelsUser.User).filter( modelsUser.User.id == request.buyer_id, modelsUser.User.role == 'Buyer').first()

                if not buyer:
                    raise HTTPException(status_code=404, detail='Buyer not found')
                db_request = models.Request(
                    title=request.title,
                    description=request.description,
                    buyer_id=request.buyer_id,
                    requestor_id=current_user.id,
                    status="Pending"
                )
                db.add(db_request)
                db.commit()
                db.refresh(db_request)
                print("-----------HALO-------------------------",db_request.id)
                # Add items to the request
                for item in request.items:
                    db_item = Item(
                        name=item.name,
                        quantity=item.quantity,
                        request_id=db_request.id
                    )
                    db.add(db_item)

                    
                db.commit()
                db.refresh(db_request)
                
                print('-----------------------2------------------------------')
                
                return db_request
            except SQLAlchemyError as e:
                db.rollback()
                return {"error": str(e)}


router = RequestRouter(req_repository, schemas.Request).router