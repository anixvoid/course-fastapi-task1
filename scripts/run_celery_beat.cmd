..\venv\scripts\activate.bat

celery --app=src.tasks.celery_app:celery_instance beat -l INFO