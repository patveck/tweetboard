
test:
	-python travistest.py
	-wget http://hg.python.org/cpython/raw-file/d047928ae3f6/Lib/test/mock_socket.py
	-node -v
	-npm version
	nosetests
