# Dockerfile para app Flask
FROM python:3.12-slim

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app /app

ENV FLASK_APP=app.py
ENV DB_HOST=db
ENV DB_PORT=3306
ENV DB_USER=root
ENV DB_PASSWORD=root
ENV DB_NAME=Obligatorio

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
