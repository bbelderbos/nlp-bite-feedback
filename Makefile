.PHONY: setup
setup:
	python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

.PHONY: lint
lint:
	flake8 --exclude venv

.PHONY: test
test:
	pytest

.PHONY: ci
ci: lint test
