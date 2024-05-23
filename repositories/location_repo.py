from models.location import Location
from repositories.crud_repo import CRUDRepository


class LocationRepository(CRUDRepository):
    def __init__(self) -> None:
        super().__init__(Location)
