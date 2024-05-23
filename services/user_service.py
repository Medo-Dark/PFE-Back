from typing import List
from fastapi import Depends, HTTPException, Query
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
        
        @self.router.post('/users-to-notify', response_model=List[dict], response_model_exclude_unset=True)
        async def get_users_to_notify(data: schemas.UserPlantDepartment , db: Session = Depends(get_db)):
           
            users= user_repository.get_users_by_plant_and_departments(db, data.plant, data.departments)
            if not users:
                raise CustomHTTPException.item_not_found('users')
            else:
                users_data = [{"username": user.username, "email": user.email} for user in users]
                return users_data
            
        @self.router.patch("/{resource_id}", response_model=Response[responseType])
        async def update_item_by_id(resource_id: int, item: schemas.UserUpdate, db: Session = Depends(get_db)):
            
            if not any(item.dict().values()):
                raise CustomHTTPException.no_fields_given()

            updated_item = repository.update_by_id(db=db, model_id=resource_id, data=item)
            if not updated_item:
                raise CustomHTTPException.item_not_found()

            return Response[responseType](data=updated_item)
        
        @self.router.post('/append-to-team', response_model=Response[responseType])
        async def append_to_team(data: schemas.AppendToTeam, db: Session = Depends(get_db)):
            try:
                updated_users = user_repository.append_to_team(users_ids=data.users_id, teams_ids=data.teams_id, db=db)
                if not updated_users:
                    raise HTTPException(status_code=404, detail="Users not found")
                return {"message": "Users added to team successfully"}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.post('/remove-users-from-teams', response_model=Response[responseType])
        async def remove_users_from_teams(data: List[schemas.TeamUserDelete], db: Session = Depends(get_db)):
            try:
                user_repository.remove_users_from_teams(data=data, db=db)
                return {"message": "Users removed from teams successfully"}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
            
router = UserRouter(user_repository, schemas.User).router
