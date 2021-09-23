PACKAGE_NAME=photo_renamer


upload: build
	.venv/bin/twine upload \
		-r testpypi \
		--username $(USERNAME) --password $(PASSWORD) \
		dist/*

build: test
	.venv/bin/python setup.py bdist_wheel

test: install
	.venv/bin/flake8
	.venv/bin/coverage run -m pytest
	.venv/bin/coverage report -m

install: venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -e .[dev,dist]

venv:
	python -m venv .venv


clean: clean_tests clean_build
	rm -rf .venv/

clean_tests:
	rm -rf .pytest_cache .coverage
	find . -name "__pycache__" -not -path "./.venv/*" | xargs -L1 rm -rf

clean_build:
	rm -rf \
		dist/ \
		build/ \
		$(PACKAGE_NAME).egg-info/