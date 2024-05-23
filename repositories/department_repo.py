from sqlalchemy.orm import Session
from models.user import Department
from repositories.crud_repo import CRUDRepository, ModelType
from repositories.user_repo import UserRepository
from schemas.user import AssignedDepartment, DepartmentUsers


class DepartmentRepository(CRUDRepository):
    def __init__(self) -> None:
        super().__init__(Department)

    def find_by_name(self, db: Session, department_name: str):
        return db.query(self.model).filter_by(name=department_name).first()

    def delete_by_name(self, db: Session, department_name: str):
        department = self.find_by_name(db, department_name=department_name)
        if department:
            self._delete(db, department)
            return department
        return None

    def assign_department_to_user(self, db: Session, assigned_department: AssignedDepartment,
                                  user_repository: UserRepository):
        user = user_repository.find_by_id(db=db, model_id=assigned_department.user_id)
        department: Department = self.find_by_name(db=db, department_name=assigned_department.department_name)

        if not user or not department:
            return None

        if department not in user.departments:
            user.departments.append(department)
            db.commit()
        return user
