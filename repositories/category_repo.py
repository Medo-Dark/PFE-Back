from models.category import Category
from repositories.crud_repo import CRUDRepository


class CategoryRepository(CRUDRepository):
    def __init__(self) -> None:
        super().__init__(Category)
