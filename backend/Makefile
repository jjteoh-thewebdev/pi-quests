install:
	pip install -r requirements.txt

dev:
	uvicorn app.main:app --reload

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000

# format:
# 	black .
# 	ruff .

test-unit:
	pytest tests/unit

test-e2e:
	pytest tests/e2e

clean:
	find . -type d -name '__pycache__' -exec rm -r {} +

.PHONY: install run format test clean