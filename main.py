from fastapi import FastAPI, Depends
import orjson
import typing
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from config.database import engine, Base
from services.user_service import router as user_router
from services.auth_service import router as auth_router
from services.request_service import router as req_router
from services.item_service import router as itm_router
from services.supplier_service import router as supp_router

from services.tst import router as tst_router



class ORJSONResponse(JSONResponse):
    media_type = "application/json"

    def render(self, content: typing.Any) -> bytes:
        return orjson.dumps(content)



app = FastAPI(default_response_class=ORJSONResponse)

Base.metadata.create_all(bind=engine)
# Include routers
app.include_router(router=auth_router)
app.include_router(router=user_router)
app.include_router(router=tst_router)
app.include_router(router=req_router)
app.include_router(router=itm_router)
app.include_router(router=supp_router)


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
