from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.datastructures import UploadFile
from fastapi.param_functions import Depends, File
from cruds.firebase_auth import GetCurrentUser
from schemas.user import UserId
from schemas.util import DeleteStatus
import os
import shutil

asset_router = APIRouter()


@asset_router.post("/", response_model=str)
async def post_asset(
    file: UploadFile = File(...),
    user: UserId = Depends(GetCurrentUser()),
):
    if file is None:
        raise HTTPException(status_code=400, detail="UploadFile is not found")

    filename = file.filename
    fileobj = file.file
    dir_path = f'./assets/{user.google_uid}/'
    os.makedirs(dir_path, exist_ok=True)

    try:
        upload_dir = open(os.path.join(dir_path, filename),'wb+')
        shutil.copyfileobj(fileobj, upload_dir)
        upload_dir.close()
        return 'success'
    except Exception as e:
        return 'failed'


@asset_router.delete("/", response_model=str)
async def delete_asset(
    slide_id: str = '',  user: UserId = Depends(GetCurrentUser())
):
    try:
        dir_path = f'./assets/{user.google_uid}/'
        os.remove(os.path.join(dir_path, f'{slide_id}.png'))

        if len(os.listdir(dir_path)) == 0:
            os.rmdir(dir_path)
        return "succes"
    except Exception as e:
        return "failed"