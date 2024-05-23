from fastapi import FastAPI, Depends
import orjson
import typing
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from auth.authentication import get_current_user
from auth.authorization import check_permissions
from config.database import engine, Base, Base_Data, engine_data
from services.user_service import router as user_router
from services.auth_service import router as auth_router
from services.problem_service import router as problem_router
from services.location_service import router as location_router
from services.department_service import router as department_router
from services.tst import router as tst_router
from services.team_service import router as team_router
from services.cause_service import router as cause_router
from services.category_service import router as category_router


class ORJSONResponse(JSONResponse):
    media_type = "application/json"

    def render(self, content: typing.Any) -> bytes:
        return orjson.dumps(content)


Base.metadata.create_all(bind=engine)
Base_Data.metadata.create_all(bind=engine_data)

app = FastAPI(default_response_class=ORJSONResponse)

# Include routers
app.include_router(router=auth_router)
app.include_router(router=user_router)
app.include_router(router=problem_router)
app.include_router(router=location_router)
app.include_router(router=department_router)
app.include_router(router=tst_router)
app.include_router(router=team_router)
app.include_router(router=cause_router)
app.include_router(router=category_router)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
