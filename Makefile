setup:
	pip install -e .

install:
	python install.py

test:
	python -m nose2 -v -B

test-integration:
	python -m nose2 -v -B -s tests/integration

test-hardware:
	python -m nose2 -v -B -s tests/hardware

test-e2e:
	python -m nose2 -v -B -s tests/e2e

test-ci:
	tox

format:
	pre-commit run --all-files

format-staged:
	pre-commit run

lint:
	flake8 --max-line-length=140 --ignore=E203,E302 src tests tasks scripts; mypy src tests tasks scripts

lint-pylint:
	pylint --fail-under=6 --rcfile=.pylintrc --disable=C0114,C0115,C0116,R0801,C0103,W0201 src tests tasks scripts

lint-mypy:
	mypy src tests tasks scripts
