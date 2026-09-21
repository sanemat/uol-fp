.PHONY: setup pdf words

setup:
	python3 -m venv .venv
	.venv/bin/pip install -e .

pdf:
	.venv/bin/python md_to_pdf.py

words:
	python3 count_words.py
