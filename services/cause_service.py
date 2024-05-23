import time
import pandas as pd
from fastapi import Depends, status, APIRouter, UploadFile, File
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from config.dependencies import get_db_data
from models.cause import Cause
from repositories.cause_repo import CauseRepository
from schemas.cause import Cause as CauseSchema
from schemas.cause import CauseBase as CauseBaseSchema
from schemas.response import Response
import polars as pl

cause_repo = CauseRepository()
router = APIRouter(prefix='/causes', tags=['Causes'])


@router.get(path='/all', response_model=Response[list[CauseSchema]])
async def get_all_causes(db: Session = Depends(get_db_data)):
    causes: list[CauseSchema] = cause_repo.find_all(db=db)
    return Response[list[CauseSchema]](status=status.HTTP_200_OK, data=causes)


@router.post("/", response_model=dict)
async def create_causes(excel_file: UploadFile = File(...), sheet_name: str = "causes",
                          db: Session = Depends(get_db_data)):
    try:
        start_time = time.time()
        cause_added, data = cause_repo.excel_read(db, excel_file, sheet_name)
        for _, row in data.iterrows():
            existing = cause_repo.get_by_criteria(db=db, type=row['type'], cause_number=row['cause_number'],
                                                     cause=row['cause'], sub_cause_number=row['sub_cause_number'], sub_cause=row['sub_cause'])
            if not existing:
                row = row.apply(lambda x: '' if pd.isna(x) else x)
                cause = CauseBaseSchema(**row.to_dict())
                cause_repo.insert_line(db, cause)
                cause_added.append(cause)
        db.close()
        end_time = time.time()

        return {"data": cause_added, "elapsed_time": end_time - start_time}

    except SQLAlchemyError as e:
        db.rollback()
        return {"error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR


@router.post("/polars", response_model=dict)
async def create_causes(excel_file: UploadFile = File(...), sheet_name: str = "causes",
                          db: Session = Depends(get_db_data)):
    try:
        start_time = time.time()
        # Read the Excel file into a Polars DataFrame
        df = pl.read_excel(excel_file.file, sheet_name=sheet_name)
        
        # Convert the Polars DataFrame to an Arrow table, then to a Python dictionary
        data = df.to_arrow().to_pydict()

        # Insert the data into the database table
         
        for i in range(len(data["type"])):
            type = data["type"][i]
            cause_number = data["cause_number"][i]
            cause = data["cause"][i]
            sub_cause_number = data["sub_cause_number"][i]
            sub_cause = data["sub_cause"][i]

            existing_line = db.query(Cause).filter_by(type=type, cause_number=cause_number, cause=cause,sub_cause_number=sub_cause_number,sub_cause=sub_cause).first()
            if existing_line:
                continue  # Skip adding if line already exists

            # If line doesn't exist, add it
            cause_line = Cause(type=type, cause_number=cause_number, cause=cause,sub_cause_number=sub_cause_number,sub_cause=sub_cause)
            
            db.add(cause_line)
        db.commit()
        end_time = time.time()

        # Calculate the elapsed time
        elapsed_time = end_time - start_time

        return {"data": "Data inserted successfully", "elapsed_time": elapsed_time}

    except SQLAlchemyError as e:
        return {"error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR

