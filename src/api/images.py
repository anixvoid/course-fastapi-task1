import os 
import shutil

from fastapi import APIRouter, UploadFile, BackgroundTasks

from src.tasks.tasks import resize_image, resize_image_celery

router = APIRouter(prefix="/images", tags=["Изображения"])

@router.post("")
def upload_image(file: UploadFile, background_tasks: BackgroundTasks):
    os.makedirs("static/images", exist_ok=True)
    
    image_path = f"static/images/{file.filename}"
    with open(image_path, "wb") as dst_file:
        shutil.copyfileobj(file.file, dst_file) 

    is_background_celery = False
    if is_background_celery:
        resize_image_celery.delay(image_path)
    else:
        background_tasks.add_task(resize_image, image_path)