from typing import TypeVar, Generic
from fastapi import status
import pandas as pd
from sqlalchemy.orm import Session
from xlrd import XLRDError
from config.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class CRUDRepository(Generic[ModelType]):
    def __init__(self, model: ModelType) -> None:
        self.model = model

    def insert_line(self, db: Session, data):
        record = self.model(**data.dict())
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    def find_by_id(self, db: Session, model_id: int) -> ModelType:
        return db.query(self.model).filter(self.model.id == model_id).first()

    def find_by_name(self, db: Session, name: str):
        return db.query(self.model).filter_by(username=name).first()

    def find_all(self, db: Session) -> list[ModelType]:
        return db.query(self.model).all()

    @staticmethod
    def _delete(db: Session, model: ModelType) -> None:
        db.delete(model)
        db.commit()

    def delete_by_id(self, db: Session, model_id: int) -> ModelType | None:
        model = self.find_by_id(db, model_id)
        if model:
            self._delete(db=db, model=model)
            return model
        return None

    def update_by_id(self, db: Session, model_id: int, data) -> ModelType | None:
        model = self.find_by_id(db, model_id)
        if model:
            update_data = {}
            for key, value in data.dict().items():
                if value is not None:  # Check if the value is not None
                    if key == "password":
                        from auth.authentication import get_password_hash
                        update_data["hashed_password"] = get_password_hash(value)
                    else:
                        update_data[key] = value
            db.query(self.model).filter(self.model.id == model_id).update(update_data)
            db.commit()
            db.refresh(model)
            return model
        return None

    def get_by_criteria(self, db, **criteria):
        return db.query(self.model).filter_by(**criteria).first()

    @staticmethod
    def excel_read(db: Session, excel_file, sheet_name: str):
        db.begin()
        try:
            df = pd.read_excel(excel_file.file, sheet_name=sheet_name)
        except XLRDError as e:
            db.rollback()
            return {"error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR

        data = df.where(pd.notnull(df), '')

        location_added = []
        return location_added, data
