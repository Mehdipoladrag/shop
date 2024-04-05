FROM python:3.12.2-alpine
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/PY/BIN:$PATH"

RUN pip install --upgrade pip


COPY . /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt


