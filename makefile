IMAGE_NAME = $(shell cat config.yml | shyaml get-value app_name)

db-up:
	docker-compose up --force-recreate -d rethink

db-down:
	docker-compose rm -fs rethink

queue-up:
	docker run --name nats -p 4222:4222 -p 8222:8222 -d nats

serve:
	python reloader.py -m lemo

build:
	docker build -t ${IMAGE_NAME} .

run:
	docker-compose up
