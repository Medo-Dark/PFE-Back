from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

import models.user as models
import schemas.user as schemas
from config.dependencies import get_db
from consts.custom_exceptions import CustomHTTPException
from repositories.user_repo import UserRepository
from schemas.response import Response
from services.base_service import BaseRouter


user_repository = UserRepository()


class UserRouter(BaseRouter[models.User, schemas.User]):
    def __init__(self, repository, responseType):
        super().__init__(responseType=responseType, repository=repository)

        @self.router.get(path='/approve/{user_id}', response_model=Response)
        async def approve_user(user_id: int, db: Session = Depends(get_db)):
            approved_user = user_repository.toggle_approve(user_id=user_id, db=db)
            if not approved_user:
                raise CustomHTTPException.item_not_found('user')
            else:
                return Response(
                    message='Approved successfully'
                )
        
        @self.router.get(path='/Buyer/Commodity/{Commodity}', response_model=List[schemas.User])
        async def get_Buyer_by_commodity(Commodity: str, db: Session = Depends(get_db)):
            db_buyers :schemas.User = db.query(models.User).filter(models.User.commodity == Commodity, models.User.role.in_(['Buyer', 'Admin'])).all()
            print(db_buyers)
            if not db_buyers:
                raise CustomHTTPException.item_not_found('user')
            else:
                return db_buyers

       

        @self.router.patch("/{resource_id}", response_model=Response[responseType])
        async def update_item_by_id(resource_id: int, item: schemas.UserUpdate, db: Session = Depends(get_db)):

            if not any(item.dict().values()):
                raise CustomHTTPException.no_fields_given()

            updated_item = repository.update_by_id(db=db, model_id=resource_id, data=item)
            if not updated_item:
                raise CustomHTTPException.item_not_found()

            return Response[responseType](data=updated_item)


router = UserRouter(user_repository, schemas.User).router
