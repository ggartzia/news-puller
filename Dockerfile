FROM python:3.7.8-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV MODEL_PATH=/model

RUN mkdir /app
COPY news_puller /app/news_puller
COPY __main__.py /app
COPY wsgi.py /app
COPY requirements.txt /app

RUN apt-get update && apt-get install gcc g++ -y && apt-get clean

WORKDIR /app

RUN pip install pip==20.0.2
RUN pip install -r requirements.txt

EXPOSE 5000

CMD python .
