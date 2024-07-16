###########################
# SETUP AND HELPERS


# PYTHON LOCAL ENVIRONMENT
PYTHON_VERSION=3.11
PROJECT=cards


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
	pip install -r ./requirements.txt

# Test commands
flake8.check:
	flake8 . --count

test:
	pytest -v
