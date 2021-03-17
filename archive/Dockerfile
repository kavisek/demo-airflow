# Pull Image from docker hub
FROM python:3.8.5-slim

# Set working directory
ENV AIRFLOW_HOME="/app"
WORKDIR /app

COPY . /app/

RUN apt-get update
RUN apt-get install postgresql postgresql-contrib -y
RUN pip install -r requirements.txt

EXPOSE 8080
