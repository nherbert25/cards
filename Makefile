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
.PHONY: setup
setup:
	python$(PYTHON_VERSION) -m venv venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -r requirements.txt
	@echo ""
	@echo "✓ Setup complete!"
	@echo "Activate the environment with: source venv/bin/activate"
	@echo "Then compile TypeScript with: make build"
	@echo "Finally run the app with: python -m cards.app"

.PHONY: venv_windows
venv_windows:
	python -m venv .venv
	.venv\Scripts\activate
	pip install -r ./requirements.txt

.PHONY: venv_windows_destroy
venv_windows_destroy:
	deactivate
	rm -r .venv

.PHONY: venv_destroy
venv_destroy:
	rm -rf venv


####################################################
####################################################
# Test commands

flake8.check:
	flake8 . --count

test:
	pytest --ignore=tests/blackjack/test_blackjack_end_to_end.py

test_all:
	pytest

coverage:
	coverage run -m pytest
	coverage report --omit="tests/*" --skip-covered --sort=Cover -m
####################################################
####################################################

####################################################
####################################################
# Build commands

# Define a build target that calls ts_compile
build: ts_compile

# compiles all ts to js using the tsconfig.json config file, required after making any changes to ts files
ts_compile:
	tsc --project ./tsconfig.json
####################################################
####################################################


####################################################
####################################################
# git shortcuts

.PHONY: preview-cleanup cleanup
# Preview merged branches that would be deleted
preview-cleanup:
	git branch --merged master | grep -v "master" | xargs -I {} echo "Would delete: {}"

# Actually delete merged branches
cleanup:
	git branch --merged master | grep -v "master" | xargs git branch -d