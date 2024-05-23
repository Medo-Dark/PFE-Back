from fastapi import UploadFile
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CheckedByBase(BaseModel):
    username: str


class CheckedByInDb(CheckedByBase):
    problem_id: int


class CheckedBy(CheckedByBase):
    id: int
    problem_id: int

    class Config:
        from_attributes = True


class CheckedByInProblem(CheckedByBase):
    id: int

    class Config:
        from_attributes = True

class ProblemInAttribute(BaseModel):
    id: int
    type: str
    description: str

    class Config:
        from_attributes = True


class AlertBase(BaseModel):
    alerted: str


class AlertInDb(AlertBase):
    pass


class Alert(AlertBase):
    id: int
    problems: List[ProblemInAttribute]

    class Config:
        from_attributes = True


class AlertInProblem(AlertBase):
    id: int

    class Config:
        from_attributes = True


class AttachmentBase(BaseModel):
    name: str
    type: str


class AttachmentInDb(AttachmentBase):
    problem_id: int


class Attachment(AttachmentBase):
    id: int
    problem_id: int

    class Config:
        from_attributes = True


class AttachmentInProblem(AttachmentBase):
    id: int

    class Config:
        from_attributes = True


class ActionBase(BaseModel):
    action: str
    time: datetime
    who: str


class ActionInDb(ActionBase):
    problem_id: int


class Action(ActionBase):
    id: int
    problem_id: int

    class Config:
        from_attributes = True


class ActionInProblem(ActionBase):
    id: int

    class Config:
        from_attributes = True


class CauseBase(BaseModel):
    cause: str
    details: str


class CauseInDb(CauseBase):
    pass


class Cause(CauseBase):
    id: int
    problems: List[ProblemInAttribute]

    class Config:
        from_attributes = True


class CauseInProblem(CauseBase):
    id: int

    class Config:
        from_attributes = True


class ProblemBase(BaseModel):
    type: str
    description: str
    details: str
    how_detected: str
    who_detected: str
    where: str
    when: datetime
    bad_pieces: int
    qte_tri: int
    qte_nok: int
    reboot_time: Optional[datetime] = None
    level: Optional[str] = "Superviseur"
    status: Optional[str] = "open"
    username: str


class ProblemInDb(ProblemBase):
    id: int


class ProblemPost(ProblemBase):
    causes: List[CauseBase]
    actions: List[ActionBase]
    attachments: List[AttachmentBase]
    alerts: List[AlertBase]


class Problem(ProblemBase):
    id: int
    causes: List[CauseInProblem]
    actions: List[ActionInProblem]
    attachments: List[AttachmentInProblem]
    checked_by: List[CheckedByInProblem]
    alerts: List[AlertInProblem]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ImagesBody(BaseModel):
    names: List[str]
    type: str

class ProblemUpdate(BaseModel):
    type: Optional[str]=None
    description: Optional[str]=None
    details: Optional[str]=None
    how_detected: Optional[str]=None
    who_detected: Optional[str]=None
    where: Optional[str]=None
    when: Optional[datetime]=None
    bad_pieces: Optional[int]=None
    qte_tri: Optional[int]=None
    qte_nok: Optional[int]=None
    reboot_time: Optional[datetime]=None
    level: Optional[str]=None
    status: Optional[str]=None
    username: Optional[str]=None
    causes: Optional[List[CauseBase]]=None
    actions: Optional[List[ActionBase]]=None
    attachments: Optional[List[AttachmentBase]]=None
    checked_by: Optional[List[CheckedByBase]]=None
    alerts: Optional[List[AlertBase]]=None



