
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . .






CMD ["/bin/bash", "-c", "alembic revision --autogenerate ; alembic upgrade head ; uvicorn main:app --host 0.0.0.0 --port 10000"]
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]