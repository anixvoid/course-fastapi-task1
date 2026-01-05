from fastapi import APIRouter, UploadFile, BackgroundTasks

from src.services.images import ImageService


router = APIRouter(prefix="/images", tags=["Изображения"])

@router.post("")
def upload_image(file: UploadFile):
    ImageService().save_image(file.filename, file.file)