clean:
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	rm -f .coverage

test: clean
	nosetests -s --rednose

coverage: clean
	nosetests --with-coverage --cover-package=lbo