"""Builds the report: renders the PDF flavour with LibreOffice, measures page numbers, fills the
table of contents and the lists of figures and tables, and tunes the layout to the target page count."""
import re
import subprocess
import sys
from pathlib import Path

from pypdf import PdfReader

sys.path.insert(0, str(Path(__file__).parent))
import build_docx as B

OUT = Path(__file__).resolve().parent.parent / "output"
TARGET = int(sys.argv[1]) if len(sys.argv) > 1 else 54
HEADER = "گزارش پروژه: طراحی و پیاده‌سازی فروشگاه اینترنتی تک‌شاپ"
STRIP = re.compile(r"[‌-‏‪-‮⁦-⁩ـ\s]|ll")


def normalise(text):
    return STRIP.sub("", text)


def to_pdf(docx):
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(OUT), str(docx)], check=True, capture_output=True, timeout=600)
    return docx.with_suffix(".pdf")


def measure(pdf, report):
    reader = PdfReader(str(pdf))
    def walk(items, acc):
        for item in items:
            if isinstance(item, list):
                walk(item, acc)
            else:
                acc[normalise(item.title)] = reader.get_destination_page_number(item)
        return acc
    outline = walk(reader.outline, {})
    first_heading = normalise(report.headings[0][1])
    body_start = outline[first_heading]
    toc = {}
    for level, text in report.headings:
        index = outline.get(normalise(text))
        if index is not None:
            toc[text] = index - body_start + 1
    lists = {}
    for kind, entries in (("شکل", report.figures), ("جدول", report.tables)):
        for number, text in entries:
            index = outline.get(normalise(f"{kind} {number}: {text}"))
            if index is not None:
                lists[(kind, number)] = index - body_start + 1
    return len(reader.pages), body_start, toc, lists


def build_pdf(overrides):
    first = B.build("pdf", OUT / "tmp.docx", overrides=overrides)
    entries = list(first.headings)
    figures, tables = first.figures, first.tables
    toc_pages, list_pages = {}, {}
    for _ in range(3):
        report = B.build("pdf", OUT / "tmp.docx", toc_pages, list_pages, entries, figures, tables, overrides)
        pdf = to_pdf(OUT / "tmp.docx")
        count, body_start, new_toc, new_lists = measure(pdf, report)
        if new_toc == toc_pages and new_lists == list_pages:
            break
        toc_pages, list_pages = new_toc, new_lists
    return count, body_start, report, len(toc_pages), len(list_pages)


if __name__ == "__main__":
    steps = [dict(body=11.0, line=1.45), dict(body=11.5, line=1.5), dict(body=12.0, line=1.5), dict(body=12.0, line=1.6), dict(body=12.5, line=1.6)]
    chosen = None
    for overrides in steps:
        overrides = {**overrides, "table": overrides["body"] - 1.5, "small": overrides["body"] - 2.0}
        count, body_start, report, n_toc, n_lists = build_pdf(overrides)
        print(overrides, "pages", count, "front", body_start, "toc", n_toc, "lists", n_lists, flush=True)
        if count >= TARGET:
            chosen = overrides
            break
    print("chosen", chosen)
