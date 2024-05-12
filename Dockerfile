# FROM python:3.11.1-slim

# WORKDIR /app

# COPY ./requirements.txt /app/requirements.txt

# RUN pip install -r /app/requirements.txt

# EXPOSE 8000
# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

# Use an official Python runtime as a parent image
FROM python:3.11

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /code
COPY . /code/
