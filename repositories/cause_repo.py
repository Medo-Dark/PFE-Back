from models.cause import Cause
from repositories.crud_repo import CRUDRepository


class CauseRepository(CRUDRepository):
    def __init__(self) -> None:
        super().__init__(Cause)

