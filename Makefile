install:
	@echo "Creating virtual environment..."
	virtualenv -p python3.8.10 venv
	@echo "Activating virtual environment..."
	. venv/bin/activate
	@echo "Installing requirements..."
	pip3 install -r requirements.txt

clean:
	@echo "Cleaning up..."
	. venv/bin/activate
	pip3 uninstall -r requirements.txt
	deactivate
	@echo "Removing virtual environment..."
	rm -rf venv

run:
	@echo "Running main.py..."
	. venv/bin/activate
	python3 generative-michigan-tracking.py
