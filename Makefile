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
.PHONY: venv_mac
venv_mac:
	pyenv install -s $(PYTHON_VERSION)
	pyenv uninstall -f $(PROJECT)
	pyenv virtualenv -f $(PYTHON_VERSION) $(PROJECT)
	pyenv local $(PROJECT)
	PYENV_VERSION=$(PROJECT)
	pip install -r ./requirements.txt

.PHONY: venv_windows
venv_windows:
	python -m venv .venv
	.venv\Scripts\activate
	pip install -r ./requirements.txt

.PHONY: venv_windows_destroy
venv_windows_destroy:
	deactivate
	rm -r .venv



# Test commands
flake8.check:
	flake8 . --count

test:
	pytest -v

coverage:
	coverage run -m pytest
	coverage report --omit="tests/*" --skip-covered --sort=Cover -m
