.PHONY: run build clean install reinstall install-local uninstall-local test help

APP_NAME = NetStat
VENV = ./venv
PYTHON = $(VENV)/bin/python

run: ## Run the app
	$(PYTHON) main.py

build: ## Build standalone macOS app
	./build.sh

clean: ## Clean build artifacts
	rm -rf build dist *.egg-info *.icns *.iconset
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

reinstall: ## Clean and reinstall venv
	rm -rf $(VENV)
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r requirements.txt

install-local: build ## Install app to /Applications
	cp -R dist/$(APP_NAME).app /Applications/

uninstall-local: ## Remove app from /Applications
	rm -rf /Applications/$(APP_NAME).app

install: ## Install dependencies
	python3 -m venv $(VENV) 2>/dev/null || true
	$(VENV)/bin/pip install -q -r requirements.txt

test: ## Run module tests
	$(PYTHON) network.py
	$(PYTHON) bandwidth.py
	$(PYTHON) config.py
	$(PYTHON) history.py

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'
