FROM python:3.9-slim

WORKDIR /persephone
COPY . .
RUN pip install -r requirements.txt
