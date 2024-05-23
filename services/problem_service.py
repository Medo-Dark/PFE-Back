from pathlib import Path
from typing import List

from fastapi.responses import FileResponse, StreamingResponse
from config.mailer import problem_notify_html_template, send_email
from fastapi import BackgroundTasks, Depends, HTTPException, Query, status, UploadFile, File
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from auth.dependencies import separate_by_type, upload_files
from config.dependencies import get_db
from config.settings import get_settings
from consts.custom_exceptions import CustomHTTPException
from models.problem import CheckedBy, Problem
from repositories.problem_repo import CheckedByRepository, ProblemRepository, CauseRepository, AlertRepository, AttachmentRepository, \
    ActionRepository
from schemas.problem import CheckedByInDb, ImagesBody, ProblemPost, ProblemBase, AttachmentInDb, ActionInDb, CauseBase, \
    AlertBase, ProblemUpdate
from schemas.problem import Problem as ProblemSchema
from schemas.response import Response
from schemas.settings import Settings
from services.base_service import BaseRouter
from utils.mailer import format_template

problem_repository = ProblemRepository()
action_repository = ActionRepository()
attachment_repository = AttachmentRepository()
alert_repository = AlertRepository()
cause_repository = CauseRepository()
checked_by_repository = CheckedByRepository()


class ProblemRouter(BaseRouter[Problem, ProblemSchema]):
    def __init__(self, repository, responseType):
        super().__init__(responseType=responseType, repository=repository)

        @self.router.post("/upload")
        async def upload_attachments(situationok: List[UploadFile] = [], situationko: List[UploadFile] = [],
                             securisation: List[UploadFile] = []):
            uploaded_files_paths = await upload_files(situationok, situationko, securisation)
            return uploaded_files_paths

        @self.router.post("", response_model=dict)
        async def create_problems(problem_full: ProblemPost, bg_tasks: BackgroundTasks,settings: Settings = Depends(get_settings), db: Session = Depends(get_db)):

            problem: ProblemBase = separate_by_type(problem_full)

            causes: List[CauseBase] = problem_full.causes

            alerts: List[AlertBase] = problem_full.alerts

            try:
                db.begin()
                saved_problem = problem_repository.insert_line(data=problem, db=db)
                for cause in causes:
                    saved_cause = cause_repository.insert_line(data=cause, db=db)
                    saved_problem.causes.append(saved_cause)

                for action in problem_full.actions:
                    action_data = ActionInDb(**action.dict(), problem_id=saved_problem.id)
                    action_repository.insert_line(data=action_data, db=db)

                for attachment in problem_full.attachments:
                    attachment_data = AttachmentInDb(**attachment.dict(), problem_id=saved_problem.id)
                    attachment_repository.insert_line(data=attachment_data, db=db)

                for alert in alerts:
                    saved_alert = alert_repository.insert_line(data=alert, db=db)
                    saved_problem.alerts.append(saved_alert)

                db.commit()

                recipients = [alert.alerted for alert in alerts]

                

                for recipient in recipients:
                    email_body = format_template(
                    problem_notify_html_template,
                    username=saved_problem.username,
                    alerted=recipient.split("@")[0].replace(".", " "),
                    description=saved_problem.description,
                    where=saved_problem.where,
                    type=saved_problem.type,
                    when=saved_problem.when
                    )
                    bg_tasks.add_task(
                    send_email,
                    recipient,
                    "Problem alert",
                    email_body, settings.MAIL
                    )

                return {
                    "status": status.HTTP_201_CREATED,
                    "data": "Problem created successfully"
                }
            except SQLAlchemyError:
                db.rollback()
                return {
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "data": "Internal Server Error"
                }

        @self.router.get("/{id}", response_model=ProblemSchema)
        async def get_problem_by_id(id: int, db: Session = Depends(get_db)):
            return problem_repository.find_by_id(db, id)

        # @self.router.post("tst", response_model=List[ProblemSchema])
        # async def get_problem_by_plant_and_alert(alert_name: List[str], plant: str, db: Session = Depends(get_db)):
        #     problems: List[ProblemSchema] = []
        #     for alert in alert_name:
        #         problems.extend(problem_repository.find_problem_by_plant_and_alert(db, plant, alert))
        #     return problems
        
        @self.router.get("/email/", response_model=List[ProblemSchema])
        async def get_problems_by_email(email ,db: Session = Depends(get_db)):
            return problem_repository.find_problems_by_alert(db, email)
        
    

        @self.router.get("/images/{image_path:path}")
        async def get_image(image_path: str):
            return FileResponse(image_path)
        
        @self.router.patch("/{resource_id}", response_model=Response[responseType])
        async def update_item_by_id(resource_id: int, item: ProblemUpdate, db: Session = Depends(get_db)):
        
            if not any(item.dict().values()):
                raise CustomHTTPException.no_fields_given()

            updated_item = problem_repository.update_by_id(db=db, model_id=resource_id, data=item)
            if not updated_item:
                raise CustomHTTPException.item_not_found()

            return Response[responseType](data=updated_item)
        
        @self.router.post("/checked-by")
        async def add_checked_by(data: CheckedByInDb, db: Session = Depends(get_db)):
            existing_record = db.query(CheckedBy).filter_by(username=data.username, problem_id=data.problem_id).first()
            if existing_record:
                return Response(message="Record already exists")
            checked_by_repository.insert_line(data=data, db=db)
            return Response(message="Checked by added successfully")

router = ProblemRouter(problem_repository, ProblemSchema).router
