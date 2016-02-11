all: cp/bootai-static cp/install-requirements
	@echo "Running all target"

env-bootai: requirements.txt
	virtualenv $@

cp/install-requirements: env-bootai requirements.txt
	env-bootai/bin/pip --version | grep 3   # heuristically check python versoin
	env-bootai/bin/pip install -r requirements.txt
	touch $@

cp/bootai-static:
	wget http://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css  -O bootai/static/lib/bootstrap.min.css
	wget http://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap-theme.min.css  -O bootai/static/lib/bootstrap-theme.min.css
	wget https://cdnjs.cloudflare.com/ajax/libs/react/0.14.6/react.js -O bootai/static/lib/react.js
	wget https://cdnjs.cloudflare.com/ajax/libs/react/0.14.6/react-dom.js -O bootai/static/lib/react-dom.js
	wget https://cdnjs.cloudflare.com/ajax/libs/babel-core/5.8.23/browser.js -O bootai/static/lib/browser.js
	wget https://cdnjs.cloudflare.com/ajax/libs/react-bootstrap/0.28.2/react-bootstrap.js -O bootai/static/lib/react-bootstrap.js
	wget https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.1/jquery.js -O bootai/static/lib/jquery.js
	wget https://cdnjs.cloudflare.com/ajax/libs/socket.io/1.4.5/socket.io.js -O bootai/static/lib/socketio.js
	@echo "Download NOT minimfied version of libraries!"
	touch $@

run-bootai: cp/install-requirements
	env-bootai/bin/python3 run_bootai.py

open-bootai:
	open http:127.0.0.1:5000


.PHONY: run-bootai open-bootai
