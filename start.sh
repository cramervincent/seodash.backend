uvicorn main:app -host 0.0.0.0 --port 10000
alembic revision --autogenerate -m 'migration'
alembic upgrade head
