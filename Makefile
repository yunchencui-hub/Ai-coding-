PY ?= python3
CRAP_THRESHOLD ?= 6
TEST_EXAMPLE = $(PY) -m pytest -q -x -p no:cacheprovider example/tests

.PHONY: help install test coverage crap mutate fence build build-check check clean

help:  ## List the targets
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  make %-12s %s\n", $$1, $$2}'

install:  ## Install the dev dependencies (pytest, coverage)
	$(PY) -m pip install pytest coverage

test:  ## Run every test (tools, build script, example shop, feature file)
	$(PY) -m pytest

coverage:  ## Run the tests under coverage and write coverage.json
	$(PY) -m coverage run -m pytest
	$(PY) -m coverage json -q -o coverage.json

crap: coverage  ## CRAP gate: fail if any function scores above $(CRAP_THRESHOLD)
	$(PY) tools/crap.py --coverage coverage.json --threshold $(CRAP_THRESHOLD) tools scripts example/shop

mutate:  ## Mutation gate: fail if any mutant of example/shop survives
	$(PY) tools/mutate.py --test "$(TEST_EXAMPLE)" example/shop

fence:  ## Dependency gate: fail if a shop module imports something it may not
	$(PY) tools/fence.py example/fence.toml

build:  ## Regenerate study/flashcards.csv and dist/ALL-INSIGHTS.md
	$(PY) scripts/build.py

build-check:  ## Fail if the generated files are stale
	$(PY) scripts/build.py --check

check: crap fence mutate build-check  ## Every gate. "Done" means this exits 0.
	@echo "All gates passed."

clean:  ## Remove coverage and cache files
	rm -rf .coverage coverage.json htmlcov .pytest_cache
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
