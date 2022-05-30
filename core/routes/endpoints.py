from fastapi import APIRouter, File, UploadFile

router = APIRouter(
    prefix="/finger-print",
    responses={404: {"description": "Not found"}},
)

# check if such fingerprint exist in databse (mongo)
@router.post("/xd1/")
async def create_files(files: list[bytes] = File()):
    return {"file_sizes": [len(file) for file in files]}


#compare two fingerpirints
@router.post("/xd2/")
async def create_upload_files(files: list[UploadFile]):


    return {"filenames": [file.filename for file in files]}
