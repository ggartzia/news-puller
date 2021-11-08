# news_puller

> Obtiene las noticias de los diferentes periodicos utilizando sus RSS.


## Requirements

* Python 3
* Pipenv `pip install pipenv`


## Setup

pipenv install --dev


## Development

docker build -t news-puller .

docker run -p 5000:5000 -d news-puller

http://localhost:5000/

List running containers:
docker ps

Watch logs:
docker logs -f <CONTAINER_ID>


### Run tests

pipenv run test

### Run linter

pipenv run lint