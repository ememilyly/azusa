FROM python:3.9-slim

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /src
COPY src .
RUN pip install /src
RUN mkdir /tests
COPY tests/ /tests/

CMD python3 bin/persephone ,
