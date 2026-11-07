import os
root = r"C:\Users\vmont\OneDrive\Desktop\2brain-vmontoya\.agents"
files = []
for dp, dn, fn in os.walk(root):
    for f in fn:
        if f.endswith(".md"):
            p = os.path.join(dp, f)
            t = open(p, "rb").read().decode("utf-8-sig")
            if any(c in t for c in ["\u00c3", "\u00c2", "\u00e2\u20ac", "\u00f0\u0178"]):
                files.append(p)
print("afectados:", len(files))
ok = 0; fail = []
for p in files:
    if p.endswith(r"rules\alfred.md"):
        continue
    t = open(p, "rb").read().decode("utf-8-sig")
    try:
        fixed = t.encode("cp1252").decode("utf-8")
    except Exception as e:
        fail.append((p, str(e))); continue
    ok += 1
    if p.endswith(r"gardener\SKILL.md"):
        print("muestra:", ascii(fixed.splitlines()[6])[:120])
print("reparables:", ok, "fallos:", len(fail))
for p, e in fail[:5]: print("  FALLO", p, e)
