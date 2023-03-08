FROM python:3.9-slim

WORKDIR /azusa
COPY . .
RUN pip install -r requirements.txt
