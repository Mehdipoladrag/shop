"""Content blocks of the report. Each helper returns a tuple that build_docx.py renders."""

def h1(text): return ("h1", text)
def h2(text): return ("h2", text)
def h3(text): return ("h3", text)
def p(text): return ("p", text)
def ul(items): return ("ul", items)
def ol(items): return ("ol", items)
def tbl(caption, headers, rows, widths=None, small=False): return ("table", caption, headers, rows, widths, small)
def fig(name, caption, width_cm=15.5): return ("fig", name, caption, width_cm)
def code(text, caption=None): return ("code", text, caption)
def note(text): return ("note", text)
def pb(): return ("pagebreak",)
