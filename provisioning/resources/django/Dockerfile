FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./provisioning/resources/django/requirements.txt /app/
COPY ./src /app/src

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "./src/manage.py", "runserver", "0.0.0.0:8000"]


