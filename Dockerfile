FROM python:3.11

WORKDIR /opt/app

COPY ./requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./skymarket/. .

COPY .env .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]