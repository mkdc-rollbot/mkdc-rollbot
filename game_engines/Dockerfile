FROM python:3.12-slim

WORKDIR /game_engines

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["uvicorn"]
