setup:
	pip install -e .

install:
	python install.py

test:
	python -m unittest discover -v && python -m unittest discover -v -p "hw_test_*.py"

format:
	pre-commit run --all-files

format-staged:
	pre-commit run
