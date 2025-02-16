FROM python:3.9-slim

WORKDIR /app

COPY . /app

ENV ALLOWED_ORIGINS=${ALLOWED_ORIGINS}

ENV CLEAR_PASSWORD=${CLEAR_PASSWORD}

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
