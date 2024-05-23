import time
import pandas as pd
from fastapi import Depends, status, APIRouter, UploadFile, File
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from config.dependencies import get_db_data
from models.location import Location
from repositories.location_repo import LocationRepository
from schemas.location import Location as LocationSchema
from schemas.location import LocationBase as LocationBaseSchema
from schemas.response import Response
import polars as pl

location_repo = LocationRepository()
router = APIRouter(prefix='/locations', tags=['Locations'])


@router.get(path='/all', response_model=Response[list[LocationSchema]])
async def get_all_locations(db: Session = Depends(get_db_data)):
    locations: list[LocationSchema] = location_repo.find_all(db=db)
    return Response[list[LocationSchema]](status=status.HTTP_200_OK, data=locations)


@router.post("/", response_model=dict)
async def create_locations(excel_file: UploadFile = File(...), sheet_name: str = "Localisation",
                          db: Session = Depends(get_db_data)):
    try:
        start_time = time.time()
        location_added, data = location_repo.excel_read(db, excel_file, sheet_name)
        for _, row in data.iterrows():
            existing = location_repo.get_by_criteria(db=db, plant=row['plant'], project=row['project'],
                                                     area=row['area'], line=row['line'])
            if not existing:
                row = row.apply(lambda x: '' if pd.isna(x) else x)
                location = LocationBaseSchema(**row.to_dict())
                location_repo.insert_line(db, location)
                location_added.append(location)
        db.close()
        end_time = time.time()

        return {"data": location_added, "elapsed_time": end_time - start_time}

    except SQLAlchemyError as e:
        db.rollback()
        return {"error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR


@router.post("/polars", response_model=dict)
async def create_locations(excel_file: UploadFile = File(...), sheet_name: str = "Localisation TFZ",
                          db: Session = Depends(get_db_data)):
    try:
        start_time = time.time()
        # Read the Excel file into a Polars DataFrame
        df = pl.read_excel(excel_file.file, sheet_name=sheet_name)
        
        # Convert the Polars DataFrame to an Arrow table, then to a Python dictionary
        data = df.to_arrow().to_pydict()

        # Insert the data into the database table
         
        for i in range(len(data["plant"])):
            plant = data["plant"][i]
            project = data["project"][i]
            area = data["area"][i]
            line = data["line"][i]

            existing_line = db.query(Location).filter_by(plant=plant,project=project,area=area,line=line).first()
            if existing_line:
                continue  # Skip adding if line already exists

            # If line doesn't exist, add it
            location = Location(plant=plant, project=project, area=area, line=line)
            
            db.add(location)
        db.commit()
        end_time = time.time()

        # Calculate the elapsed time
        elapsed_time = end_time - start_time

        return {"data": "Data inserted successfully", "elapsed_time": elapsed_time}

    except SQLAlchemyError as e:
        return {"error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR

