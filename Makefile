setup:
	pip install -e .

install:
	python install.py

test:
	python -m unittest discover -v

format:
	pre-commit run --all-files

format-staged:
	pre-commit run
