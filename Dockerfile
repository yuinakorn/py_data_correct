FROM python:3.11.1-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]