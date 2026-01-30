.PHONY: install check lint test test-integration

install:
	./.venv/bin/python -m pip install -U pip setuptools wheel
	./.venv/bin/python -m pip install -e . --force-reinstall
	./.venv/bin/python -m pip install -U pytest ruff

check:
	./.venv/bin/python -c "import frd; print('OK:', frd.__file__)"

lint: install
	./.venv/bin/python -m ruff check .

test: install check
	./.venv/bin/python -m pytest -q -m "not integration"

test-integration: install check
	./.venv/bin/python -m pytest -q -m integration
