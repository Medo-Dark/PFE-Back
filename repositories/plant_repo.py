from sqlalchemy.orm import Session
from models.user import Plant
from repositories.crud_repo import CRUDRepository
from repositories.user_repo import UserRepository
from schemas.user import AssignedPlant


class PlantRepository(CRUDRepository):
    def __init__(self) -> None:
        super().__init__(Plant)

    def find_by_name(self, db: Session, plant_name: str):
        return db.query(self.model).filter_by(name=plant_name).first()

    def delete_by_name(self, db: Session, plant_name: str):
        plant = self.find_by_name(db, plant_name=plant_name)
        if plant:
            self._delete(db, plant)
            return plant
        return None

    def assign_plant_to_user(self, db: Session, assigned_plant: AssignedPlant,
                             user_repository: UserRepository):
        user = user_repository.find_by_id(db=db, model_id=assigned_plant.user_id)
        plant: Plant = self.find_by_name(db=db, plant_name=assigned_plant.plant_name)

        if not user or not plant:
            return None

        if plant not in user.plants:
            user.plants.append(plant)
            db.commit()
        return user
