###########################
# SETUP AND HELPERS


# PYTHON LOCAL ENVIRONMENT
PYTHON_VERSION=3.11
PROJECT=cards

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
	pip install -r ./requirements.txt

# Test commands
flake8.check:
	flake8 . --count

test:
	pytest -v
