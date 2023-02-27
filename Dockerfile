FROM python:3.9-slim-buster

WORKDIR app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 4000

CMD [ "python", "manage.py", "runserver", "--host=0.0.0.0", "--port=4000"]

#ref : https://dev.to/francescoxx/build-a-crud-rest-api-in-python-using-flask-sqlalchemy-postgres-docker-28lo