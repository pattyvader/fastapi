FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /v1/app

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

COPY . .
COPY ./v1/app /v1/app
COPY .env .env

EXPOSE 5000

CMD ["uvicorn", "music_api:app", "--host", "0.0.0.0", "--port", "5000" ]