# use python 3.11 as base image
FROM python:3.11

WORKDIR /app

VOLUME /app

RUN pip install -r requirements.txt

CMD ["bash", "run.sh"]