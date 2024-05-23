import time
import pandas as pd
from fastapi import Depends, status, APIRouter, UploadFile, File
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from config.dependencies import get_db_data
from models.category import Category
from repositories.category_repo import CategoryRepository
from schemas.category import Category as CategorySchema
from schemas.category import CategoryBase as CategoryBaseSchema
from schemas.response import Response
import polars as pl

category_repo = CategoryRepository()
router = APIRouter(prefix='/categories', tags=['Categories'])


@router.get(path='/all', response_model=Response[list[CategorySchema]])
async def get_all_categories(db: Session = Depends(get_db_data)):
    categories: list[CategorySchema] = category_repo.find_all(db=db)
    return Response[list[CategorySchema]](status=status.HTTP_200_OK, data=categories)


@router.post("/", response_model=dict)
async def create_categories(excel_file: UploadFile = File(...), sheet_name: str = "category",
                          db: Session = Depends(get_db_data)):
    try:
        start_time = time.time()
        category_added, data = category_repo.excel_read(db, excel_file, sheet_name)
        for _, row in data.iterrows():
            existing = category_repo.get_by_criteria(db=db, type=row['type'], code=row['code'],
                                                     category=row['category'], sub_category=row['sub_category'])
            if not existing:
                row = row.apply(lambda x: '' if pd.isna(x) else x)
                category = CategoryBaseSchema(**row.to_dict())
                category_repo.insert_line(db, category)
                category_added.append(category)
        db.close()
        end_time = time.time()

        return {"data": category_added, "elapsed_time": end_time - start_time}

    except SQLAlchemyError as e:
        db.rollback()
        return {"error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR


@router.post("/polars", response_model=dict)
async def create_categories(excel_file: UploadFile = File(...), sheet_name: str = "category",
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
            code = data["code"][i]
            category = data["category"][i]
            sub_category = data["sub_category"][i]

            existing_line = db.query(Category).filter_by(type=type,code=code,category=category,sub_category=sub_category).first()
            if existing_line:
                continue  # Skip adding if line already exists

            # If line doesn't exist, add it
            category_line = Category(type=type,code=code,category=category,sub_category=sub_category)
            
            db.add(category_line)
        db.commit()
        end_time = time.time()

        # Calculate the elapsed time
        elapsed_time = end_time - start_time

        return {"data": "Data inserted successfully", "elapsed_time": elapsed_time}

    except SQLAlchemyError as e:
        return {"error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR

