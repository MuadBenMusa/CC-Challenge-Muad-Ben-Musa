.PHONY: up down logs reset migrate-up migrate-down migrate-new migrate-status data import-data

up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f

reset:
	docker compose down -v
	docker compose up -d postgres

migrate-up:
	docker compose --profile tools run --rm dbmate up

migrate-down:
	docker compose --profile tools run --rm dbmate down

migrate-new:
	docker compose --profile tools run --rm dbmate new initial-schema

migrate-status:
	docker compose --profile tools run --rm dbmate status

data:
	docker compose --profile tools build faker
	docker compose --profile tools run --rm faker

import-data:
	docker compose --profile tools build faker
	docker compose --profile tools run --rm faker python import_data.py
