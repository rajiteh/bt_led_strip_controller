IMAGE ?= led-hack:latest

build:
	poetry export --format=requirements.txt --without-hashes --output=requirements.txt
	docker build -t ${IMAGE} .

run:
	uvicorn led_hack.web:app --reload --host 0.0.0.0