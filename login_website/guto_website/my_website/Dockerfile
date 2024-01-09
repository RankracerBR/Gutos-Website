FROM python:3.11.5

RUN apt-get update && apt-get install -y cmake libgl1-mesa-glx

WORKDIR /code

COPY requirements.txt /code/
RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r requirements.txt


COPY .env /code/.env

# Comando para iniciar o servidor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
