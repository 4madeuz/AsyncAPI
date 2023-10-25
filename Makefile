run:
	poetry run uvicorn src.services.main:app --reload

up:
	docker compose up -d

build:
	docker compose up -d --build

lint:
	poetry run pflake8