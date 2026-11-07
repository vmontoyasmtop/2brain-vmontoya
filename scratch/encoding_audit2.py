import os, json
root = r"C:\Users\vmont\OneDrive\Desktop\2brain-vmontoya"
skip = {".git", "node_modules", "tools", ".venv"}
bad = []
count = 0
for dp, dn, fn in os.walk(root):
    dn[:] = [d for d in dn if d not in skip]
    for f in fn:
        if not f.endswith((".md", ".ps1", ".py", ".json", ".txt")):
            continue
        p = os.path.join(dp, f)
        count += 1
        try:
            t = open(p, "rb").read().decode("utf-8")
        except UnicodeDecodeError:
            bad.append((p, "NO-UTF8", 0)); continue
        n = sum(t.count(c) for c in ["\u00c3", "\u00c2", "\u00e2\u20ac", "\u00f0\u0178"])
        if n:
            bad.append((p, "mojibake", n))
print(f"Analizados: {count} | Afectados: {len(bad)}")
for p, k, n in sorted(bad, key=lambda x: -x[2])[:45]:
    print(f"{n:4} {k:8} {p.replace(root+os.sep,'')}")
print("\n--- MUESTRAS ascii() ---")
for rel in [".agents/skills/alfred/SKILL.md", "wiki/index.md", "wiki/log.md", ".agents/skills/gardener/SKILL.md"]:
    p = os.path.join(root, rel)
    t = open(p, "rb").read().decode("utf-8")
    line = t.splitlines()[6] if rel.endswith("SKILL.md") else t.splitlines()[0]
    print(rel, "=>", ascii(line[:90]))
