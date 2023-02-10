
FROM python:3.9

WORKDIR /code
ADD start.sh /
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . .
# CMD ["alembic", "revision ", "--autogenerate", "-m", "migration"]
# CMD ["alembic", "upgrade", "head"]
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]


RUN chmod 001 ./start.sh

CMD ["./start.sh"]

