
from typing import List
from sqlalchemy import or_
from sqlalchemy.orm import Session

from repositories.crud_repo import CRUDRepository
from models.user import Team, User
from schemas.user import TeamUserDelete


class UserRepository(CRUDRepository):
    def __init__(self) -> None:
        super().__init__(User)

    def find_by_username_or_email(self, db: Session, username: str | None = None, email: str | None = None):
        return (
            db.query(self.model)
            .filter((self.model.username == username) | (self.model.email == email))
            .first()
        )

    def toggle_approve(self, db: Session, user_id: int):
        user: User = self.find_by_id(db, user_id)
        if not user:
            return None
        user.account_status = not user.account_status
        db.commit()
        return user

    def update_password(self, db: Session, email: str, new_password: str):
        user: User = self.find_by_username_or_email(db, email=email)
        if not user:
            return None
        user.hashed_password = new_password
        db.commit()
        return user
    
    def get_users_by_plant_and_departments(self, db: Session, plant: str, departments: List[str]):
        users: List[User] = db.query(self.model).filter(
            self.model.plants.any(name=plant),
            or_(*(self.model.departments.any(name=department) for department in departments))
        ).all()
        return users

    def append_to_team(self, users_ids: List[int], teams_ids: List[int], db: Session):
        for user_id in users_ids:
            user: User = db.query(User).filter(User.id == user_id).first()
            if not user:
                continue  # Skip if the user is not found
            for team_id in teams_ids:
                team: Team = db.query(Team).filter(Team.id == team_id).first()
                if team and team not in user.teams:
                    user.teams.append(team)
        db.commit()
        return True
    
    def remove_users_from_teams(self, data: List[TeamUserDelete], db: Session):
        for item in data:
            user: User = db.query(User).filter(User.username == item.username).first()
            if not user:
                continue
            team: Team = db.query(Team).filter(Team.id == item.team_id).first()
            if not team:
                continue
            user.teams.remove(team)
        db.commit()
        return True
    
        


