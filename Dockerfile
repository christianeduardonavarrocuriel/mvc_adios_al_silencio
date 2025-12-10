FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY aplicacion ./aplicacion

# Variables de entorno embebidas en la imagen
ENV SUPABASE_URL=https://uyvyaeuedqbrzgzddcrl.supabase.co \
	SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV5dnlhZXVlZHFicnpnemRkY3JsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQ5NjE5MDUsImV4cCI6MjA4MDUzNzkwNX0.E3h7yUXbPVimNHtvpq5MImPuyINDMB9Ux2gE0zqF0Pc

EXPOSE 8080

CMD ["python", "aplicacion/app.py"]
