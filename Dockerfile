
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN alembic revision --autogenerate
RUN alembic upgrade head
COPY . .



CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]




