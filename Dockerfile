FROM python:3.9-slim

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /src
COPY src/ .
RUN pip install -e /src
RUN mkdir /tests
COPY tests/ /tests/


#CMD python3 run.py
