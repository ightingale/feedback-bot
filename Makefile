
project_dir := .

# Lint code
.PHONY: lint
lint:
	@poetry run black --check --diff $(project_dir)
	@poetry run ruff check $(project_dir)
	@poetry run mypy $(project_dir) --strict

# Reformat code
.PHONY: reformat
reformat:
	@poetry run black $(project_dir)
	@poetry run ruff check $(project_dir) --fix


# Make database migration
.PHONY: migration
migration:
	poetry run alembic revision \
	  --autogenerate \
	  --rev-id $(shell python migrations/_get_next_revision_id.py) \
	  --message $(message)

.PHONY: migrate
migrate:
	poetry run alembic upgrade head

.PHONY: app-build
app-build:
	docker compose build

.PHONY: app-run-db
app-run-db:
	docker compose stop
	docker compose up -d redis postgres --remove-orphans

.PHONY: app-run
app-run:
	docker compose stop
	docker compose up -d --remove-orphans

.PHONY: app-stop
app-stop:
	docker compose stop

.PHONY: app down
app-down:
	docker compose down

.PHONY: app-destroy
app-destroy:
	docker compose down -v --remove-orphans

.PHONY: app-logs
app-logs:
	docker compose logs -f bot

.PHONY: save-logs
save-logs:
	docker compose logs bot > bot.log

.PHONY: app-pull
app-pull:
	$(MAKE) save-logs
	git pull
	$(MAKE) app-build
	$(MAKE) app-run
