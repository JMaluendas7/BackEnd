FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential cmake libopenblas-dev liblapack-dev libx11-dev libgtk-3-dev && \
    pip install --upgrade pip

COPY ./requirements.txt ./

RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
