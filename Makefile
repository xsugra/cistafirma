.PHONY: help clean lint format

# ====================================================================================
# HELPERS
# ====================================================================================

help:
	@echo "Makefile for Django development"
	@echo ""
	@echo "Available commands:"
	@echo "  make venv"
	@echo "      Create a virtual environment and install dependencies"
	@echo "  make runserver"
	@echo "      Run the Django development server"
	@echo "  make migrations"
	@echo "      Create new database migrations"
	@echo "  make migrate"
	@echo "      Apply database migrations"
	@echo "  make superuser"
	@echo "      Create a new superuser"
	@echo "  make test"
	@echo "      Run the test suite"
	@echo "  make lint"
	@echo "      Run the linter"
	@echo "  make format"
	@echo "      Format the code"
	@echo "  make freeze"
	@echo "      Freeze the current dependencies to requirements.txt"
	@echo "  make clean"
	@echo "      Remove temporary files"


# ====================================================================================
# DEVELOPMENT
# ====================================================================================

VENV_DIR=venv
PYTHON=$(VENV_DIR)/bin/python
PIP=$(VENV_DIR)/bin/pip

venv: $(VENV_DIR)/bin/activate

$(VENV_DIR)/bin/activate: requirements.txt
	python3 -m venv $(VENV_DIR)
	$(PIP) install -r requirements.txt
	touch $(VENV_DIR)/bin/activate

runserver: venv
	$(PYTHON) source/manage.py runserver "localhost:8000"

migrations: venv
	$(PYTHON) source/manage.py makemigrations

migrate: venv
	$(PYTHON) source/manage.py migrate

superuser: venv
	$(PYTHON) source/manage.py createsuperuser

test: venv
	$(PYTHON) source/manage.py test

lint: venv
	$(PYTHON) -m ruff check .

format: venv
	$(PYTHON) -m ruff format .

freeze: venv
	$(PIP) freeze > requirements.txt

clean:
	@rm -rf .cache
	@rm -rf htmlcov coverage.xml .coverage
	@find . -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@rm -rf $(VENV_DIR)
