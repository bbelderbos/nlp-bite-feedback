.PHONY: setup
setup:
	uv sync

.PHONY: db
db:
	createdb reviews && psql -U postgres -d reviews -f data.sql

.PHONY: lint
lint:
	uvx ruff check

.PHONY: test
test:
	uv run pytest

.PHONY: ci
ci: lint test
