from models.user import Team
from repositories.crud_repo import CRUDRepository


class TeamRepository(CRUDRepository):
    def __init__(self) -> None:
        super().__init__(Team)

    def find_by_name(self, db, name: str):
        return db.query(self.model).filter_by(name=name).first()