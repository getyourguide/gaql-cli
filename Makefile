.PHONY: develop
develop:
	poetry install

.PHONY: dist
dist: clean
	poetry build
	poetry publish

.PHONY: clean
clean:
	rm -rf build dist *egg-info

.PHONY: lint
lint:
	poetry run flake8
	make format

.PHONY: format
format:
	poetry run black -l 100 -S gaql
