PYTHON=".env/bin/python"

init:
	python3 -m venv .env

source: init
	. .env/bin/activate

install: source
	.env/bin/pip install -r requirements.txt

build-docker:
	docker build -t seth-hobson/backhacker .

run:
	docker run -ti -v`pwd`:/app -d -e ENVIRONMENT=production backhacker

test_keltner_aapl: source
	${PYTHON} main.py --symbol1 SPY --strategy keltner_channel --start-date 2020-08-01 --plot True --stake 10 --cash 30000
