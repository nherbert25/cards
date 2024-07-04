###########################
# SETUP AND HELPERS


# PYTHON LOCAL ENVIRONMENT
PYTHON_VERSION=3.11
PROJECT=cards
PYPI_INDEX_URL=https://pypi.org/simple

check_defined = \
    $(strip $(foreach 1,$1, \
        $(call __check_defined,$1,$(strip $(value 2)))))
__check_defined = \
    $(if $(value $1),, \
      $(error Undefined $1$(if $2, ($2))))


###########################
# DOCKER BUILD AND PUSH TO ECR


###########################
# LOCAL PYTHON AND UNIT-TEST ENV
#
.PHONY: venv
venv:
	pyenv install -s $(PYTHON_VERSION)
	pyenv uninstall -f $(PROJECT)
	pyenv virtualenv -f $(PYTHON_VERSION) $(PROJECT)
	pyenv local $(PROJECT)
	PYENV_VERSION=$(PROJECT)
	pip install --upgrade pip setuptools wheel keyring --index-url $(PYPI_INDEX_URL)
	pip install -r ./cards/requirements.txt
	pip install -r ./tests/requirements.txt

# Test commands
flake8.check:
	flake8 . --count

test:
	make test.unit
	make test.component
	make test.integration
	make test.system_integration

test.unit:
	pytest --cov-config=.coveragerc --cov=src tests --junitxml=coverage/junit.xml -v -m unit

test.component:
	pytest --cov-config=.coveragerc --cov=src tests --junitxml=coverage/junit.xml -v -m component

test.integration:
	pytest --cov-config=.coveragerc --cov=src tests --junitxml=coverage/junit.xml -v -m integration

test.system_integration:
	pytest --cov-config=.coveragerc --cov=src tests --junitxml=coverage/junit.xml -v -m system_integration

# CI commands
ci.test.unit:
	flit install
	make test.unit

ci.test.component:
	flit install
	make test.component

ci.test.integration:
	flit install
	make test.integration

ci.test.system_integration:
	flit install
	make test.system_integration

ci.test.all.local:
	make ci.test.unit && make ci.test.component && make ci.test.integration && make ci.test.system_integration

