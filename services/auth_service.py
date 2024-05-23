from fastapi import Depends, APIRouter, status, BackgroundTasks, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from auth.authentication import verify_token, generate_tokens, create_reset_password_token, \
    get_password_hash
from config.mailer import reset_pwd_html_template, send_email
from consts import static_exceptions as exceptions
from auth.dependencies import get_user_to_save, get_authenticated_user
from config.settings import Settings, get_settings
from config.dependencies import get_db
from repositories.department_repo import DepartmentRepository
from repositories.plant_repo import PlantRepository
from repositories.user_repo import UserRepository
from schemas.response import Response
from schemas.user import (User, Token, TokenVerificationSettings, ForgetPasswordRequest,
                          ResetPasswordTokenVerificationRequest, ResetPasswordRequest,
                          AssignedDepartment, UserDepartment, AssignedPlant)
from utils.mailer import format_template

user_repository = UserRepository()
department_repository = DepartmentRepository()
plant_repository = PlantRepository()
router = APIRouter(prefix='/auth', tags=['Auth'])


# Register A User
@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=Response[User])
async def register(user: UserDepartment = Depends(get_user_to_save),
                   db: Session = Depends(get_db)):
    if not user:
        raise exceptions.credentials_already_taken
    userindb, user = user
    try:
        db.begin()
        saved_user: User = user_repository.insert_line(data=userindb, db=db)
        for plant in user.plants:
            user_plant: AssignedPlant = AssignedPlant(plant_name=plant, user_id=saved_user.id)
            plant_repository.assign_plant_to_user(
                assigned_plant=user_plant,
                user_repository=user_repository,
                db=db
            )
        for department in user.departments:
            user_department: AssignedDepartment = AssignedDepartment(department_name=department, user_id=saved_user.id)
            department_repository.assign_department_to_user(
                assigned_department=user_department,
                user_repository=user_repository,
                db=db
            )

    except SQLAlchemyError:
        db.rollback()
        raise exceptions.transaction_failed
    else:
        db.commit()
        return Response[User](
            status_code=status.HTTP_201_CREATED,
            data=saved_user
        )


# Login
@router.post(path="/login", status_code=status.HTTP_200_OK, response_model=Response)
async def login_for_tokens(
        authenticated_user: User = Depends(get_authenticated_user),
        settings: Settings = Depends(get_settings)
):
    if not authenticated_user:
        raise exceptions.incorrect_credentials
    if not authenticated_user.account_status:
        raise exceptions.account_not_approved

    access_token, refresh_token = generate_tokens(user=authenticated_user, settings=settings.JWT)

    return Response[Token](
        data=Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
    )


@router.get(path="/refresh-token", status_code=status.HTTP_200_OK, response_model=Response)
async def refresh_access_token(token: str, db: Session = Depends(get_db), settings: Settings = Depends(get_settings)):
    sett = TokenVerificationSettings(
        token=token,
        key=settings.JWT.REFRESH_SECRET,
        algorithm=settings.JWT.ALGORITHM
    )
    username = await verify_token(sett)
    if not username:
        raise exceptions.invalid_token
    user: User = user_repository.find_by_username_or_email(username=username, db=db)
    if not user:
        raise exceptions.incorrect_credentials

    access_token, refresh_token = generate_tokens(user=user, settings=settings.JWT)

    return Response[Token](
        data=Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
    )


@router.post(path="/forget-password", status_code=status.HTTP_200_OK, response_model=Response)
async def forget_password(fpr: ForgetPasswordRequest, bg_tasks: BackgroundTasks,
                          settings: Settings = Depends(get_settings), db: Session = Depends(get_db)):
    try:
        user = user_repository.find_by_username_or_email(email=fpr.email, db=db)
        if user is None:
            raise exceptions.invalid_email

        secret_token = create_reset_password_token(email=fpr.email, settings=settings.JWT)
        forget_url_link = f"http://{settings.APP_HOST}:{settings.APP_FRONT_PORT}/reset-password?token={secret_token}"

        email_body = format_template(
            reset_pwd_html_template,
            username=user.username,
            link_expiry_min=int(settings.FORGET_PASSWORD_LINK_EXPIRE_MINUTES),
            reset_link=forget_url_link
        )

        bg_tasks.add_task(
            send_email,
            user.email,
            "Password Reset Instructions",
            email_body, settings.MAIL
        )

        return Response(
            message="Email has been sent"
        )

    except Exception as e:
        raise e


@router.post(path="/verify-rp-token", status_code=status.HTTP_200_OK, response_model=Response)
async def verify_reset_password_token(
        rptvr: ResetPasswordTokenVerificationRequest,
        settings: Settings = Depends(get_settings),
):
    try:
        token_verif_settings = TokenVerificationSettings(
            token=rptvr.token,
            key=settings.JWT.FORGET_PWD_SECRET,
            algorithm=settings.JWT.ALGORITHM
        )

        email = await verify_token(token_verif_settings)

        if not email:
            raise exceptions.invalid_token

        return Response[ForgetPasswordRequest](
            data=ForgetPasswordRequest(email=email),
            message="Token verified successfully"
        )

    except Exception as e:
        raise e


@router.post(path="/reset-password", status_code=status.HTTP_200_OK, response_model=Response)
async def reset_password(
        rpr: ResetPasswordRequest,
        db: Session = Depends(get_db)
):
    try:
        if rpr.new_password != rpr.confirm_password:
            raise exceptions.passwords_mismatch
        new_hashed_password = get_password_hash(password=rpr.new_password)
        user_repository.update_password(
            email=rpr.email,
            new_password=new_hashed_password,
            db=db
        )

        return Response(
            message="Password updated successfully",
        )

    except Exception as e:
        raise e
