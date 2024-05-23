from tempfile import SpooledTemporaryFile
import uuid
from pathlib import Path
from typing import Annotated, List, Union
from fastapi import Depends, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth.authentication import get_password_hash, verify_password
from config.dependencies import get_db
from repositories.user_repo import UserRepository
from schemas.problem import ProblemBase, ProblemPost
from schemas.user import UserInDb, UserDepartment

user_repository = UserRepository()


def get_user_to_save(user: UserDepartment, db: Session = Depends(get_db)):
    found_user = user_repository.find_by_username_or_email(
        username=user.username,
        email=user.email,
        db=db
    )
    db.commit()
    if not found_user:
        hashed_password = get_password_hash(user.password)
        user_data = user.dict()
        user_data['hashed_password'] = hashed_password
        return UserInDb(**user_data), user
    else:
        return None


def get_authenticated_user(login_req: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    if "@" in login_req.username:
        found_user: UserInDb = user_repository.find_by_username_or_email(
            email=login_req.username,
            db=db
        )
    else:
        found_user: UserInDb = user_repository.find_by_username_or_email(
            username=login_req.username,
            db=db
        )

    if not found_user:
        return False
    if not verify_password(login_req.password, found_user.hashed_password):
        return False
    return found_user


def separate_by_type(problem_full: ProblemPost):
    problem: ProblemBase = ProblemBase(type=problem_full.type, description=problem_full.description,
                                       details=problem_full.details, how_detected=problem_full.how_detected,
                                       who_detected=problem_full.who_detected, where=problem_full.where,
                                       when=problem_full.when, bad_pieces=problem_full.bad_pieces,
                                       qte_tri=problem_full.qte_tri, qte_nok=problem_full.qte_nok,
                                       reboot_time=problem_full.reboot_time, level=problem_full.level,
                                       status=problem_full.status, username=problem_full.username)

    return problem


async def upload_files(situationok: List[UploadFile], situationko: List[UploadFile], securisation: List[UploadFile]):
    uploaded_files_paths = []

    for file_item in situationok:
        if file_item.file:  # check if the file is not empty
            unique_filename = str(uuid.uuid4()) + Path(file_item.filename).suffix
            file_path = Path("uploads/situationok") / unique_filename
            with open(file_path, "wb") as file_object:
                file_object.write(await file_item.read())
            uploaded_files_paths.append({"name": str(unique_filename), "type": "situationok"})

    for file_item in situationko:
        if file_item.file:  # check if the file is not empty
            unique_filename = str(uuid.uuid4()) + Path(file_item.filename).suffix
            file_path = Path("uploads/situationko") / unique_filename
            with open(file_path, "wb") as file_object:
                file_object.write(await file_item.read())
            uploaded_files_paths.append({"name": str(unique_filename), "type": "situationko"})

    for file_item in securisation:
        if file_item.file:  # check if the file is not empty
            unique_filename = str(uuid.uuid4()) + Path(file_item.filename).suffix
            file_path = Path("uploads/securisation") / unique_filename
            with open(file_path, "wb") as file_object:
                file_object.write(await file_item.read())
            uploaded_files_paths.append({"name": str(unique_filename), "type": "securisation"})

    return uploaded_files_paths