.PHONY: setup install test check run clean

setup:
	pip install -e ".[test]"

install:
	pip install -e ".[test]"

test:
	python -m pytest -q

check:
	python -m compileall -q src tests
	python -m pytest -q

run:
	python -m jev.cli ord-1001 sku-shirt refund "The shirt arrived damaged" --requested-on 2026-09-20

clean:
	python -c "from pathlib import Path; [p.unlink() for p in Path('.').rglob('*.pyc')]; [p.rmdir() for p in Path('.').rglob('__pycache__') if p.exists()]"
