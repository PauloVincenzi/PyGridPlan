"""Compara bancadas: por pedido, nota mÃ©dia/mÃ­n/mÃ¡x, Ã¡rea mÃ©dia e tempo. Uso: python compare.py arq1.jsonl [arq2 ...]"""

import json
import sys
from collections import defaultdict

rows = defaultdict(list)
for path in sys.argv[1:]:
    for line in open(path, encoding="utf-8-sig"):
        j = json.loads(line)
        rows[j["request"]].append(j)

for req, runs in rows.items():
    print(req)
    for j in runs:
        s = [a["score"] for a in j["alts"]]
        ar = [a["area"] for a in j["alts"]]
        p1 = [c for c in j["calls"] if c["status"] == "FEASIBLE"]
        print(f"  {j['label']:<14} t={j['total']:6.1f}s  nota mÃ©d {sum(s)/len(s):.3f} mÃ­n {min(s):.3f} mÃ¡x {max(s):.3f}"
              f"  Ã¡rea mÃ©d {sum(ar)/len(ar):.3f}  notas {'/'.join(f'{x:.3f}' for x in s)}"
              f"  plantas {','.join(a['plan'] for a in j['alts'])}"
              + (f"  fase1 dtime {min(c['dtime'] for c in p1):.1f}-{max(c['dtime'] for c in p1):.1f}" if p1 else ""))

