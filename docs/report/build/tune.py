import sys
sys.argv = ["x", "54"]
import make_report as M
body, line = 11.5, 1.45
o = dict(body=body, line=line, table=body - 1.5, small=body - 2.0)
count, front, report, nt, nl = M.build_pdf(o)
print("pages", count, "front", front, "toc", nt, "lists", nl, flush=True)
