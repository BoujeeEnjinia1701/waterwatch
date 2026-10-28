"""Write the claims table of docs/01b-stem-check.md (WWT-STM-001) from docs/04-calcs/stem_results.csv.

Run from the repo root after docs/04-calcs/stem_check.py:  python docs/04-calcs/stm_table.py
Replaces everything between <!-- STM_TABLE --> and <!-- /STM_TABLE --> so the document and the check never
disagree. Rows are listed option by option (S, then B, then C), in the order the check script writes them.
"""
import csv
import re
from pathlib import Path

DOC = Path("docs/01b-stem-check.md")
rows = list(csv.DictReader(Path("docs/04-calcs/stem_results.csv").open()))
order = {"S": 0, "B": 1, "C": 2}
rows.sort(key=lambda r: (order[r["id"][0]], int(r["id"][1:])))
esc = lambda t: t.replace("|", "/")
lines = ["| # | Claim | Field | Branch | Governing law or source | First-order check | Verdict | Closed by |",
         "| --- | --- | --- | --- | --- | --- | --- | --- |"]
for r in rows:
    lines.append(f"| {r['id']} | {esc(r['claim'])} | {r['field']} | {r['branch']} | {esc(r['law'])} | {esc(r['check'])} | {r['verdict']} | {esc(r['closed_by']) or 'Open'} |")
text = DOC.read_text(encoding="utf-8")
new = re.sub(r"<!-- STM_TABLE -->.*?<!-- /STM_TABLE -->", "<!-- STM_TABLE -->\n" + "\n".join(lines) + "\n<!-- /STM_TABLE -->", text, flags=re.S)
DOC.write_text(new, encoding="utf-8")
n = {v: sum(r["verdict"] == v for r in rows) for v in sorted({r["verdict"] for r in rows})}
print(f"wrote {len(rows)} rows to {DOC}: {n}")
