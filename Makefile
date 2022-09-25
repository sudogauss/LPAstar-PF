VENV = lpastar_venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip3

VERSION=0.0.1
PACKAGE=lpastar_pf
ARTIFACT="$(PACKAGE)/dist/$(PACKAGE)-$(VERSION)-py3-none-any.whl"


.PHONY: test build install clean


$(VENV)/bin/activate: requirements.txt
	if [ ! -d "./lpastar_venv" ]; then python3 -m venv lpastar_venv; fi
	$(PIP) install -r requirements.txt

test: $(VENV)/bin/activate
	pytest

$(ARTIFACT): $(VENV)/bin/activate test
	$(PYTHON) -m build $(PACKAGE)

build: $(VENV)/bin/activate test
	$(PYTHON) -m build $(PACKAGE)

install: $(ARTIFACT)
	$(PIP) install $(ARTIFACT)

clean:
	rm -rf $(PACKAGE)/dist
	rm -rf .pytest_cache
	rm -rf __pycache__
