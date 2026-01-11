docker network create network

docker run --name booking_db -p 6432:5432  -e POSTGRES_USER=postgres  -e POSTGRES_PASSWORD=postgres!!!  -e POSTGRES_DB=booking   --network=network --volume pg-booking-data:/var/lib/postgresql/data      -d postgres:16
docker run --name booking_cache -p 7379:6379 --network network -d redis:7.4

docker build -t booking_image .

docker run --name booking_celery_worker --network network booking_image celery --app=src.tasks.celery_app:celery_instance worker -l INFO --pool=solo
docker run --name booking_celery_beat   --network network booking_image celery --app=src.tasks.celery_app:celery_instance beat -l INFO

docker run --name booking_service -p 8888:8000 --network network booking_image


docker start booking_db
docker start booking_cache
docker start booking_celery_worker
docker start booking_celery_beat
docker start booking_service

Service docs URL: http://127.0.0.1:8888/docs