from typing import Optional
from pydantic import BaseModel


class CauseBase(BaseModel):
    type: str
    cause_number: Optional[int] = None
    cause: Optional[str] = None
    sub_cause_number: Optional[int] = None
    sub_cause: Optional[str] = None


class Cause(CauseBase):
    id: int

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


