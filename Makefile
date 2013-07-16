
test:
	-ls -l /home/travis/virtualenv/python3.3/lib/python3.3
	-ls -l /usr/lib/python3.3
	nosetests
	npm test
