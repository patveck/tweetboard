
test:
# The Travis Python environment apparently doesn't contain test/mock_socket.py (from the standard
# library), so we download it to a local directory. We have to put an empty file __init__.py to 
# make Python recognize this directory.
ifeq ($(TRAVIS),true)
	wget -x -nH --cut-dirs=4 http://hg.python.org/cpython/raw-file/d047928ae3f6/Lib/test/mock_socket.py
	touch test/__init__.py
endif
	# Run server tests (the Python code):
	nosetests
	# Install dependencies from the "devDependencies" key in package.json:
	npm install
	# Run client tests (client-side Javascript via Karma):
	npm test
