clean:
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "*.DS_Store" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@find . -name "*.cache" -type d | xargs rm -rf
	@find . -name "*htmlcov" -type d | xargs rm -rf
	@rm -f .coverage
	@rm -f coverage.xml

test: clean
	nosetests -s --rednose

coverage: clean
	nosetests --with-coverage --cover-package=lbo

build-eb: clean
	if [ -a luizalabs-employee-manager.zip ] ; then rm luizalabs-employee-manager.zip ; fi;
	zip luizalabs-employee-manager.zip -r * .[^.]*
	zip -d luizalabs-employee-manager __MACOSX/\*