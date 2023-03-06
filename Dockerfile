FROM python:3.11.1-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade -r /app/requirements.txt

CMD ["python", "manage.py", "runserver"]