# Dockerfile

FROM python:3.10.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Install MySQL client
RUN apt-get update && apt-get install -y default-libmysqlclient-dev

# Copy project
COPY . /code/
