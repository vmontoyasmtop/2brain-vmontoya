# -*- coding: utf-8 -*-
import os
root = r"C:\Users\vmont\OneDrive\Desktop\2brain-vmontoya"
targets = []
for base in [os.path.join(root, ".agents"), os.path.join(root, "agents")]:
    for dp, dn, fn in os.walk(base):
        for f in fn:
            if f.endswith(".md"):
                targets.append(os.path.join(dp, f))
targets.append(os.path.join(root, "AGENTS.md"))
targets.append(os.path.join(root, "README.md"))
targets.append(os.path.join(root, "sync.ps1"))
bad = []
for p in targets:
    b = open(p, "rb").read()
    try:
        t = b.decode("utf-8")
    except UnicodeDecodeError as e:
        bad.append((p, "NO-UTF8", 0)); continue
    n = sum(t.count(c) for c in ["\u00c3", "\u00c2", "\u00e2\u20ac", "\u00f0\u0178"])
    if n:
        bad.append((p, "mojibake", n))
print(f"Total archivos analizados: {len(targets)}")
print(f"Afectados: {len(bad)}")
for p, kind, n in sorted(bad, key=lambda x: -x[2]):
    print(f"{n:4}  {kind:9}  {p.replace(root + os.sep, '')}")
