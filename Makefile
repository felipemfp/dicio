VERSION=$(shell git describe --tags `git rev-list --tags --max-count=1`)
PIPENV=pipenv run

install:
	@pipenv install

test:
	@$(PIPENV) python setup.py test

minor:
	@$(PIPENV) bumpversion --current-version $(VERSION) minor setup.py dicio/__init__.py

major:
	@$(PIPENV) bumpversion --current-version $(VERSION) major setup.py dicio/__init__.py

patch:
	@$(PIPENV) bumpversion --current-version $(VERSION) patch setup.py dicio/__init__.py

build: clean
	@$(PIPENV) python setup.py sdist bdist_wheel

clean:
	@rm -r dist Dicio.egg-info build

upload: build
	@$(PIPENV) twine upload --repository-url https://test.pypi.org/legacy/ dist/*

release:
	@$(PIPENV) twine upload dist/*

.PHONY: install test minor major path build clean upload release