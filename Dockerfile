FROM python:3.8

COPY . ./

ARG flask_app_secret=''

ARG google_cloud_api_secret=''

ENV FLASK_APP_SECRET_KEY=$flask_app_secret

ENV GOOGLE_CLOUD_API_KEY=$google_cloud_api_secret

RUN pip3 install -U pip setuptools

RUN pip3 --no-cache-dir install -r requirements.txt

CMD [ "python", "./install.py" ]

EXPOSE 5000

RUN pip install gunicorn

CMD gunicorn --bind :$PORT run_server:app
