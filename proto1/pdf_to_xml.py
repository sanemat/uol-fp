"""Convert a PDF to TEI XML using a local GROBID server."""

import argparse
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

import requests

GROBID_URL = "http://localhost:8070/api/processFulltextDocument"
NS = {"tei": "http://www.tei-c.org/ns/1.0"}


def convert(pdf_path: Path, out_path: Path, grobid_url: str) -> None:
    with pdf_path.open("rb") as f:
        resp = requests.post(
            grobid_url,
            files={"input": (pdf_path.name, f, "application/pdf")},
            timeout=120,
        )
    resp.raise_for_status()

    out_path.write_text(resp.text, encoding="utf-8")

    root = ET.fromstring(resp.text)
    title = root.findtext(".//tei:titleStmt/tei:title", namespaces=NS) or "(no title)"
    abstract_el = root.find(".//tei:abstract", NS)
    abstract_len = (
        len("".join(abstract_el.itertext())) if abstract_el is not None else 0
    )
    sections = root.findall(".//tei:body//tei:div", NS)

    print(f"Title   : {title}")
    print(f"Abstract: {abstract_len} chars")
    print(f"Sections: {len(sections)}")
    for div in sections:
        head = div.findtext("tei:head", namespaces=NS) or "(no heading)"
        print(f"  - {head}")


def main() -> None:
    parser = argparse.ArgumentParser(description="PDF → TEI XML via local GROBID")
    parser.add_argument("pdf", type=Path, help="Input PDF file")
    parser.add_argument(
        "--out", type=Path, default=None, help="Output XML file (default: <pdf>.xml)"
    )
    parser.add_argument("--url", default=GROBID_URL, help="GROBID endpoint URL")
    args = parser.parse_args()

    pdf_path: Path = args.pdf
    if not pdf_path.exists():
        print(f"Error: {pdf_path} not found", file=sys.stderr)
        sys.exit(1)

    out_path: Path = args.out or pdf_path.with_suffix(".xml")
    convert(pdf_path, out_path, args.url)
    print(f"Saved  : {out_path}")


if __name__ == "__main__":
    main()
