.PHONY: setup build install clean


setup: requirements.txt
	if [ ! -d "./lpastar_venv" ]; then python3 -m venv lpastar_venv; fi
	source ./lpastar_venv/bin/activate
	pip3 install -r requirements.txt

build:
	(cd ./lpastar_pf && python3 -m build)

install:
	pip3 install ./lpastar_pf/dist/lpastar_pf-0.0.1-py3-none-any.whl

clean:
	rm -rf ./lpastar_pf/dist
	rm -rf .pytest_cache
	rm -rf __pycache__
