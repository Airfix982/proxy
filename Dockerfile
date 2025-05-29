FROM python:3.10-slim

WORKDIR /app

COPY ./src ./src
COPY configure.py .
COPY .env .
COPY requirements.txt .

RUN pip install --no-cache -r requirements.txt

EXPOSE 8888
ENV PYTHONPATH=/app
CMD ["python", "./configure.py"]