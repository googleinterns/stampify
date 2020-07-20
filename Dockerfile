FROM python:3.8

COPY . ./

ARG google_cloud_api_secret=''

ENV GOOGLE_CLOUD_API_KEY=$google_cloud_api_secret

RUN pip3 install -U pip setuptools

RUN pip3 --no-cache-dir install -r requirements.txt

CMD [ "python", "./install.py" ]

RUN python -m spacy download en_core_web_sm

RUN python -c "from sentence_transformers import SentenceTransformer; model = SentenceTransformer(\"bert-base-nli-stsb-mean-tokens\")"

RUN python -c "import nltk; nltk.download(\"punkt\")"

RUN pip install gunicorn

CMD gunicorn --bind :$PORT run_server:app
