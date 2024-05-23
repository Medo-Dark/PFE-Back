from typing import Optional
from pydantic import BaseModel


class CategoryBase(BaseModel):
    type: str
    code: Optional[int] = None
    category: Optional[str] = None
    sub_category: Optional[str] = None


class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


