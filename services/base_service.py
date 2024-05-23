from typing import Generic, TypeVar, Type
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from auth.authentication import get_current_user
from config.dependencies import get_db
from consts.custom_exceptions import CustomHTTPException

from repositories.crud_repo import CRUDRepository
from schemas.response import Response
from schemas.user import User, UserUpdate

ModelType = TypeVar("ModelType")
ResponseType = TypeVar("ResponseType")


class BaseRouter(Generic[ModelType, ResponseType]):
    def __init__(self, responseType: Type[ResponseType], repository: CRUDRepository[ModelType]):
        self.responseType = responseType
        self.router = APIRouter(prefix=f'/{repository.model.__name__.lower()}s', tags=[f"{repository.model.__name__}s"])

        @self.router.get("/all", response_model=Response[list[responseType]], name=f'All {responseType.__name__}s')
        async def all_items(db: Session = Depends(get_db)):
            items: list[responseType] = repository.find_all(db=db)
            if not items:
                raise CustomHTTPException.no_items_found(repository.model.__name__)

            return Response[list[responseType]](status=status.HTTP_200_OK, data=items)

        @self.router.get("/me", response_model=ResponseType, name=f'Get current {responseType.__name__}')
        async def get_this_user(user: User = Depends(get_current_user)):
            item: responseType = user
            if not item:
                raise CustomHTTPException.item_not_found(repository.model.__name__)

            return Response[responseType](
                data=item
            )

        @self.router.get("/{resource_id}", response_model=Response[responseType],
                         name=f'Get {responseType.__name__} by id')
        async def read_item_by_id(resource_id: int, db: Session = Depends(get_db)):
            item: responseType = repository.find_by_id(db=db, model_id=resource_id)
            if not item:
                raise CustomHTTPException.item_not_found(repository.model.__name__)

            return Response[responseType](data=item)

        @self.router.get("/username/{name}", response_model=Response[responseType],
                         name=f'Get {responseType.__name__} by username')
        async def read_item_by_name(name: str, db: Session = Depends(get_db)):
            item: responseType = repository.find_by_name(db=db, name=name)
            if not item:
                raise CustomHTTPException.item_not_found(repository.model.__name__)

            return Response[responseType](data=item)

        

        @self.router.delete("/{resource_id}", response_model=Response, name=f'Delete {responseType.__name__} by id')
        async def delete_item_by_id(resource_id: int, db: Session = Depends(get_db)):
            item = repository.delete_by_id(db=db, model_id=resource_id)
            if not item:
                raise CustomHTTPException.item_not_found(repository.model.__name__)

            return Response(
                message='Deleted successfully'
            )
