rebuild:
	killall python; python build.py && (cd _build/ && python -m SimpleHTTPServer)&
