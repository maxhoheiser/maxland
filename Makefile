setup:
	pip install -e .

install:
	python install.py

test:
	python -m unittest discover -v && python -m unittest discover -v -p "hw_test_*.py"

test-ci:
	tox

format:
	pre-commit run --all-files

format-staged:
	pre-commit run
