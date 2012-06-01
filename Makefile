rebuild:
	killall python; python bin/build.py && (cd _build/ && python -m SimpleHTTPServer)&
