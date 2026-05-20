GROBID_VERSION := 0.8.1
GROBID_PORT := 8070

.PHONY: grobid-start grobid-stop grobid-wait lint format test notebook

grobid-start:
	docker run -d --rm -p $(GROBID_PORT):8070 --name grobid lfoppiano/grobid:$(GROBID_VERSION)

grobid-stop:
	docker stop grobid

grobid-wait:
	@until curl -sf http://localhost:$(GROBID_PORT)/api/isalive > /dev/null 2>&1; do sleep 2; done
	@echo "GROBID ready at http://localhost:$(GROBID_PORT)"

lint:
	ruff check src/ 2pipeline.ipynb

format:
	ruff format src/ 2pipeline.ipynb

test:
	python -m pytest tests/

notebook:
	.venv/bin/python -m jupyter lab 2pipeline.ipynb
