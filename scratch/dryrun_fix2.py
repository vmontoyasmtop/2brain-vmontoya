import os, re
root = r"C:\Users\vmont\OneDrive\Desktop\2brain-vmontoya\.agents"
LEAD = "\u00c3\u00c2\u00f0\u00e2"
TAIL = "\u0080-\u00ff\u0152\u0153\u0160\u0161\u0178\u017d\u017e\u0192\u02c6\u02dc\u2013\u2014\u2018\u2019\u201a\u201c\u201d\u201e\u2020\u2021\u2022\u2026\u2030\u2039\u203a\u20ac\u2122"
RUN = re.compile(f"[{LEAD}][{TAIL}]+")

def fix_run(run):
    for enc in ("cp1252", "latin-1"):
        try:
            b = run.encode(enc)
        except UnicodeEncodeError:
            continue
        try:
            return b.decode("utf-8")
        except UnicodeDecodeError:
            continue
    return run

def fix(t, depth=3):
    for _ in range(depth):
        new = RUN.sub(lambda m: fix_run(m.group(0)), t)
        if new == t:
            break
        t = new
    return t

bad = []
for dp, dn, fn in os.walk(root):
    for f in fn:
        if not f.endswith(".md"): continue
        p = os.path.join(dp, f)
        t = open(p, "rb").read().decode("utf-8-sig")
        if not RUN.search(t): continue
        fixed = fix(t)
        remaining = len(RUN.findall(fixed))
        bad.append((p, remaining))
        if p.endswith(r"gardener\SKILL.md"):
            print("ANTES :", ascii(t.splitlines()[6])[:110])
            print("DESPUES:", ascii(fixed.splitlines()[6])[:110])
        if p.endswith(r"project-manager\SKILL.md"):
            print("PM ANTES :", ascii(t.splitlines()[6])[:110])
            print("PM DESPUES:", ascii(fixed.splitlines()[6])[:110])
print("archivos con runs:", len(bad))
print("quedan con runs:", sum(1 for _, r in bad if r))
for p, r in bad:
    if r: print("  RESTAN", r, p)
