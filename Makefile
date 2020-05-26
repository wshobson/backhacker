init:
	python3 -m venv .env

source:
    source .env/bin/activate

install:
	pip install -r requirements.txt

build-docker:
	docker build -t seth-hobson/backhacker .

run:
	docker run -ti -v`pwd`:/app -d -e ENVIRONMENT=production backhacker