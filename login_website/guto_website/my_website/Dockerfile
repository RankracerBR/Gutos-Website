FROM python:3.9.7

RUN apt-get update && apt-get install -y cmake libgl1-mesa-glx

WORKDIR /code

COPY requirements.txt /code/
RUN python -m pip install --no-cache-dir -r requirements.txt


COPY . /code/

# Comando para iniciar o servidor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
