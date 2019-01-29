.PHONY: all lint test test-cov install dev clean distclean

all: ;

lint:
	flake8

# test: all
# 	py.test

# test-cov: all
# 	py.test --cov=q2_diversity_lib

install:
	python setup.py install

dev: all
	pip install -e .

uninstall-dev:
	pip uninstall q2-diversity-lib

clean: distclean

distclean: ;
