FROM python:3.9-slim-buster

WORKDIR /app


RUN apt-get update \
    && apt-get install -y build-essential libffi-dev libssl-dev python3-dev \
    && pip install --no-cache-dir python-telegram-bot==13.7 telegram faunadb pytz


COPY . .


CMD ["python", "main.py"]
