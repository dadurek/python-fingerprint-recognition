from typing import Optional

from fastapi import APIRouter, UploadFile

from services.fingerprint import save_file, remove_file, compare_with_user, compare_fingerprints

router = APIRouter()


@router.get("/")
async def create_upload_files():
    return {"hello": "world"}


# check if such fingerprint exist in database directory
@router.post("/compare-with-user")
async def compare_with_database(upload_file: UploadFile, username: str):
    uploaded_file_path: str = await save_file(upload_file=upload_file, username=None)
    result = compare_with_user(username, uploaded_file_path)
    await remove_file(uploaded_file_path)
    return {"match": result}


# compare two fingerprints
@router.post("/compare")
async def create_upload_files(upload_file_1: UploadFile, upload_file_2: UploadFile):
    uploaded_file_path_1: str = await save_file(upload_file=upload_file_1, username=None)
    uploaded_file_path_2: str = await save_file(upload_file=upload_file_2, username=None)
    score = compare_fingerprints(uploaded_file_path_1, uploaded_file_path_2)
    await remove_file(uploaded_file_path_1)
    await remove_file(uploaded_file_path_2)
    return {"score": score}


# add new user with fingerprint or random photo :D
@router.post("/add-file")
async def register_new_user(upload_file: UploadFile, username: str):
    await save_file(upload_file=upload_file, username=username)
    return {"message": 'OK'}

