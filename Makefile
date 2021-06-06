PYTHON="venv/bin/python"

init:
	python3 -m venv venv

source: init
	. venv/bin/activate

install: source
	.env/bin/pip install -r requirements.txt

build-docker:
	docker build -t backhacker .

run:
	docker run -ti -v`pwd`:/app -d -e ENVIRONMENT=production -e ALPACA_KEY=${ALPACA_KEY} -e ALPACA_SECRET=${ALPACA_SECRET} backhacker

test_keltner_spy: source
	${PYTHON} main.py --symbol1 SPY --strategy keltner_channel --start-date 2020-08-01 --plot True --stake 10 --cash 30000
