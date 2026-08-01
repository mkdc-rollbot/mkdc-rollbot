FROM python:3.12-slim

WORKDIR /game_engines

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "src.dnd5e.service:app", "--host", "0.0.0.0", "--port", "11039"]
