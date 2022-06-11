FROM python:3.9

RUN apt update && apt upgrade -y
RUN apt install python3-pip -y

COPY . /app
WORKDIR /app

RUN pip3 install --upgrade pip
RUN pip3 install -U -r requirements.txt
RUN python3 -m spacy download en_core_web_sm

EXPOSE 5000

CMD gunicorn -w 1 main:app
