import os 
import shutil

from fastapi import APIRouter, UploadFile

from src.tasks.tasks import resize_image

router = APIRouter(prefix="/images", tags=["Изображения"])

@router.post("")
def upload_image(file: UploadFile):
    os.makedirs("static/images", exist_ok=True)
    
    image_path = f"static/images/{file.filename}"
    with open(image_path, "wb") as dst_file:
        shutil.copyfileobj(file.file, dst_file) 

    resize_image.delay(image_path)
    #resize_image(image_path)