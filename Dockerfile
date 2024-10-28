FROM python:3.9-slim

WORKDIR /app
ADD . /app

RUN python3 -m pip install --no-cache-dir requests supabase tenacity flask

EXPOSE 80

CMD ["python3", "app.py"]
