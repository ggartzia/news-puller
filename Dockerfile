FROM python:3.9

RUN apt update && apt upgrade -y
RUN apt install python3-pip -y

COPY . /app
WORKDIR /app

RUN pip3 install --upgrade pip
RUN pip3 install -U -r requirements.txt

EXPOSE 5000

CMD gunicorn -w 4 main:app
