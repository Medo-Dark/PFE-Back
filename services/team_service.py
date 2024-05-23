from typing import List
from fastapi import Depends, HTTPException, status
from config.dependencies import get_db
from models.user import Team as TeamModel
from repositories.team_repo import TeamRepository
from schemas.user import Team as TeamSchema, TeamBase
from services.base_service import BaseRouter
from sqlalchemy.orm import Session

team_repository = TeamRepository()


class TeamRouter(BaseRouter[TeamModel, TeamSchema]):
    def __init__(self, repository, responseType):
        super().__init__(responseType=responseType, repository=repository)

        @self.router.post(path='', response_model=dict)
        async def create_team(team: TeamBase, db: Session = Depends(get_db)):
            found_team = team_repository.find_by_name(name=team.name, db=db)
            if found_team:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Team already exists'
                )

            team = team_repository.insert_line(data=team, db=db)
            return {'id': team.id, 'name': team.name}
        
        @self.router.post(path='/delete-team', response_model=dict)
        async def delete_teams(teams_id: List[int], db: Session = Depends(get_db)):
            for team_id in teams_id:
                team_repository.delete_by_id(db=db, model_id=team_id)
            return {'message': 'Teams deleted successfully'}



router= TeamRouter(team_repository, TeamSchema).router