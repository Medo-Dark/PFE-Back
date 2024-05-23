from typing import List

from sqlalchemy.orm import Session

from models.problem import CheckedBy, Problem, Action, Alert, Attachment, Cause
from repositories.crud_repo import CRUDRepository


class ProblemRepository(CRUDRepository):
    def __init__(self) -> None:
        super().__init__(Problem)

    def find_by_name(self, db, problem_name: str):
        return db.query(self.model).filter_by(name=problem_name).first()

    def delete_by_name(self, db, problem_name: str):
        problem = self.find_by_name(db, problem_name=problem_name)
        if problem:
            self._delete(db, problem)
            return problem
        return None

    def find_by_type(self, db: Session, problem_type: str):
        return db.query(self.model).filter_by(type=problem_type).first()

    def find_by_alerted(self, db: Session, alerted: bool):
        return db.query(self.model).filter_by(alerted=alerted).all()

    def find_problem_by_plant_and_alert(self, db: Session, plant_name: str, alert_name: str) -> List[Problem]:
        return db.query(Problem).filter(Problem.where == plant_name, Problem.alerts.any(alerted=alert_name)).all()

    def find_problems_by_alert(self, db: Session, alert_name: str):
        return db.query(Problem).filter(Problem.alerts.any(alerted=alert_name)).all()

class ActionRepository(CRUDRepository):
    def __init__(self) -> None:
        super().__init__(Action)


class CauseRepository(CRUDRepository):
    def __init__(self) -> None:
        super().__init__(Cause)


class AttachmentRepository(CRUDRepository):
    def __init__(self) -> None:
        super().__init__(Attachment)


class AlertRepository(CRUDRepository):
    def __init__(self) -> None:
        super().__init__(Alert)


class CheckedByRepository(CRUDRepository):
    def __init__(self) -> None:
        super().__init__(CheckedBy)