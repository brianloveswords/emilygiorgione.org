build:
	@python bin/build.py

open: build
	@killall python; \
		(cd _build/ && python -m SimpleHTTPServer)& \
		sleep 2; \
		open http://localhost:8000

kill:
	@killall python

.PHONY: build open kill