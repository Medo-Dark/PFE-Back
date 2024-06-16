import uuid
from pathlib import Path
from typing import List
from fastapi import APIRouter, UploadFile, File
from starlette.responses import JSONResponse, FileResponse

# from auth.dependencies import upload_files

router = APIRouter(prefix='/tst', tags=['TST'])

#
# @router.post("/upload")
# async def upload_fil(situationok: List[UploadFile] = File(...), situationko: List[UploadFile] = File(...),
#                      securisation: List[UploadFile] = File(...)):
#     uploaded_files_paths = await upload_files(situationok, situationko, securisation)
#     return JSONResponse(content={"uploaded_files_paths": uploaded_files_paths}, status_code=200)