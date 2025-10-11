import os

from time import sleep
from PIL import Image

from src.tasks.celery_app import celery_instance

@celery_instance.task
def test_task():
    sleep(5)
    print("Готово")

@celery_instance.task
def resize_image(image_path: str):
    sizes = [1000, 500, 200]
    output_folder = "static/images"
    img = Image.open(image_path)

    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for size in sizes:
        img_resized = img.resize((size, int(img.height * (size/img.width))), Image.LANCZOS)
        new_file_name = f"{name}_{size}px{ext}"

        output_path = os.path.join(output_folder, new_file_name)
        img_resized.save(output_path)