
# DIRECTORIES
ROOT_DIR:=./
SRC_DIR:=./src
VENV_BIN_DIR:="venv/bin"

VIRTUALENV:=$(shell which virtualenv)

REQUIREMENTS:="requirements.txt"

PIP:="$(VENV_BIN_DIR)/pip"

CMD_FROM_VENV:="$. $(VENV_BIN_DIR)/activate; which"
PYTHON:=$(shell "$(CMD_FROM_VENV)" "python")

hello:
	@echo "Hello, world!"

# DOCKER
docker:
	@docker-compose build
	@docker-compose up

updocker:
	@docker-compose up --build --force-recreate

downdocker:
	@docker compose down

restartdocker:
	@docker-compose restart

# DEVELOPMENT
define create-venv
python3 -m venv venv
endef

venv:
	@$(create-venv)
	@$(PIP) install -r $(REQUIREMENTS)
	@source venv/bin/activate

freeze:
	@$(PIP) freeze > $(REQUIREMENTS)

clean:
	@rm -rf .cache
	@rm -rf htmlcov coverage.xml .coverage
	@find . -name *.pyc -delete
	@find . -type d -name __pycache__ -delete
	@find . -path "*.sqlite3"  -delete
	@rm -rf venv
	@rm -rf .venv
	@rm -rf .tox

# TOOLS & SCRIPTS
migrations: venv
	@$(PYTHON) source/manage.py makemigrations

migrate: venv
	@$(PYTHON) source/manage.py migrate

superuser: venv
	@$(PYTHON) source/manage.py createsuperuser

runserver: venv
	@$(PYTHON) source/manage.py runserver "localhost":8000