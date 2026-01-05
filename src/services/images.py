import os
import shutil
from typing import BinaryIO

from src.services.base import BaseService
from src.tasks.tasks import resize_image, resize_image_celery

class ImageService(BaseService):
    def save_image(self, file_name: str, file_data: BinaryIO):
        os.makedirs("static/images", exist_ok=True)

        image_path = f"static/images/{file_name}"
        with open(image_path, "wb") as dst_file:
            shutil.copyfileobj(file_data, dst_file)

        resize_image_celery.delay(image_path)