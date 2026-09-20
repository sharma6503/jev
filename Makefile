.PHONY: setup install test check run examples clean

setup:
	uv sync --extra test

install:
	uv sync --extra test

test:
	uv run pytest -q

check:
	uv run python -m compileall -q src tests
	uv run pytest -q

run:
	uv run python -m jev.cli ord-1001 sku-shirt refund "The shirt arrived good" --requested-on 2026-09-20

examples:
	uv run python -m jev.examples

clean:
	uv run python -c "from pathlib import Path; [p.unlink() for p in Path('.').rglob('*.pyc')]; [p.rmdir() for p in Path('.').rglob('__pycache__') if p.exists()]"
