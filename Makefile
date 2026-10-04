.PHONY: run test coverage clean

run:
	python3 -m src.data_model

test:
	python3 -m pytest tests/ -v

coverage:
	coverage run -m pytest tests/
	coverage report -m

clean:
	rm -f journal.log
	rm -rf .coverage htmlcov .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} +