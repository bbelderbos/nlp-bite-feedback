.PHONY: setup
setup:
	uv sync

.PHONY: lint
lint:
	uvx ruff check

.PHONY: test
test:
	uv run pytest

.PHONY: ci
ci: lint test
