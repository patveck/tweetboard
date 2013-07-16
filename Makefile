
test:
ifeq ($(TRAVIS),true)
	wget -x -nH --cut-dirs=4 http://hg.python.org/cpython/raw-file/d047928ae3f6/Lib/test/mock_socket.py
endif
	nosetests
	npm install
	npm test
