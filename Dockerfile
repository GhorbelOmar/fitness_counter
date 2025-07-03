FROM python:3.13-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir uv

RUN uv pip install --no-cache-dir --system -r requirements.txt

EXPOSE 8000

CMD ["python", "run.py"]
