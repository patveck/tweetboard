
test:
	-ls -l /usr/lib/python3.3/test
	nosetests
	npm install
	npm test
