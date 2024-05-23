from typing import Optional
from pydantic import BaseModel


class LocationBase(BaseModel):
    plant: str
    project: Optional[str] = None
    area: Optional[str] = None
    line: Optional[str] = None


class Location(LocationBase):
    id: int

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


