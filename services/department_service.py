from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from config.dependencies import get_db
from repositories.department_repo import DepartmentRepository
from repositories.user_repo import UserRepository
from schemas.response import Response
from schemas.user import DepartmentUsers, DepartmentCreate, AssignedDepartment
from services.base_service import BaseRouter
from models.user import Department as Department

department_repository = DepartmentRepository()
user_repository = UserRepository()


class DepartmentRouter(BaseRouter[Department, DepartmentUsers]):
    def __init__(self, repository, responseType):
        super().__init__(responseType=responseType, repository=repository)

        # Get All Departments
        @self.router.get(path='')
        async def all_departments(db: Session = Depends(get_db)):
            return department_repository.find_all(db=db)

        # Get Department By Name
        @self.router.get('/{department_name}')
        async def get_by_name(department_name: str, db: Session = Depends(get_db)):
            department = department_repository.find_by_name(department_name=department_name, db=db)
            if department is not None:
                return department
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Department not found'
                )

        # Save Department
        @self.router.post(path='')
        async def add_department(department: DepartmentCreate, db: Session = Depends(get_db)):
            found_department = department_repository.find_by_name(department_name=department.name, db=db)
            if found_department:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Department already exists'
                )

            department = department_repository.insert_line(data=department, db=db)
            return department

        # Assign Department
        @self.router.post('/assign-department')
        async def assign_department(assigned_department: AssignedDepartment, db: Session = Depends(get_db)):
            result = department_repository.assign_department_to_user(
                assigned_department=assigned_department,
                user_repository=user_repository,
                db=db
            )
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='User or department not found'
                )

            return Response(
                status_code=status.HTTP_200_OK
            )

        @self.router.delete('/{department_name}')
        async def delete_department_by_name(department_name: str, db: Session = Depends(get_db)):
            deleted_department = department_repository.delete_by_name(department_name=department_name, db=db)
            if not deleted_department:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'Department with name {department_name} not found'
                )
            else:
                return {"detail": "Deleted successfully"}


router = DepartmentRouter(department_repository, DepartmentUsers).router
