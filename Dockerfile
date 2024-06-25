# use python 3.11 as base image
FROM python:3.11

RUN pip install -r requirements.txt

WORKDIR /app

VOLUME /app

CMD ["bash", "run.sh"]