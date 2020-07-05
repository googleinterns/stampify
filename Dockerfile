FROM python:3.8

COPY . ./

RUN pip3 install -U pip setuptools

RUN pip3 --no-cache-dir install -r requirements.txt

CMD [ "python", "./install.py" ]

EXPOSE 5000

ENTRYPOINT ["python"]
CMD ["run_server.py"]
