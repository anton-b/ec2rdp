VENV_DIR = venv

PYTHON = python3
ACTIVATE = . $(VENV_DIR)/bin/activate

$(VENV_DIR)/bin/activate:
	$(PYTHON) -m venv $(VENV_DIR) && \
	$(ACTIVATE)

# Install dependencies
install: $(VENV_DIR)/bin/activate .env
	pip install --upgrade pip setuptools wheel uv
	$(ACTIVATE) && uv pip install -r requirements.txt
	@echo '-------------------------------------------------------------'
	@echo 'run ". $(VENV_DIR)/bin/activate" to activate the virtual environment'
	@echo '-------------------------------------------------------------'

# Clean the virtual environment
clean:
	rm -rf $(VENV_DIR)

.env:
	cp .env.example .env
