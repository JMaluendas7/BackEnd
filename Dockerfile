FROM python:3.11.3

# Instalar las dependencias necesarias, incluyendo el ODBC Driver 17 para SQL Server
RUN apt-get update && apt-get install -y \
    unixodbc \
    unixodbc-dev \
    libgl1-mesa-glx \
    mesa-utils \
    && rm -rf /var/lib/apt/lists/*

# Descargar e instalar el ODBC Driver 17 para SQL Server
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE=mysite.settings

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
