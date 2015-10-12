all: build

build: Applications/Tunnit.app

Applications/Tunnit.app:
	/usr/bin/python2.7 setup.py py2app -A -s -d ./Applications

clean:
	-@rm -r build dist Applications/* 2>/dev/null || true

install:
	cp -r Applications/Tunnit.app /Applications/Tunnit.app
