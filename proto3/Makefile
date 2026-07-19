GROBID_VERSION := 0.8.1
GROBID_PORT := 8070

.PHONY: grobid-start grobid-stop grobid-wait lint format test notebook baseline sync-scoring

grobid-start:
	docker run -d --rm -p $(GROBID_PORT):8070 --name grobid lfoppiano/grobid:$(GROBID_VERSION)

grobid-stop:
	docker stop grobid

grobid-wait:
	@until curl -sf http://localhost:$(GROBID_PORT)/api/isalive > /dev/null 2>&1; do sleep 2; done
	@echo "GROBID ready at http://localhost:$(GROBID_PORT)"

lint:
	.venv/bin/ruff check src/ 3pipeline.ipynb

format:
	.venv/bin/ruff format src/ 3pipeline.ipynb

test:
	.venv/bin/pytest tests/

sync-scoring:
	.venv/bin/python sync_scoring.py

notebook:
	.venv/bin/jupyter lab 3pipeline.ipynb

baseline:
	.venv/bin/jupyter lab baseline.ipynb
