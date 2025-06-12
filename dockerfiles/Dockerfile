FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app
COPY requirements-dev.txt /app

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY . /app

EXPOSE 80

CMD ["uvicorn", "project_name.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]