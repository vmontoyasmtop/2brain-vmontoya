import os, re, codecs
root = r"C:\Users\vmont\OneDrive\Desktop\2brain-vmontoya\.agents"
LEAD = "\u00c3\u00c2\u00f0\u00e2"
TAIL = "\u0080-\u00ff\u0152\u0153\u0160\u0161\u0178\u017d\u017e\u0192\u02c6\u02dc\u2013\u2014\u2018\u2019\u201a\u201c\u201d\u201e\u2020\u2021\u2022\u2026\u2030\u2039\u203a\u20ac\u2122"
RUN = re.compile(f"[{LEAD}][{TAIL}]+")

# reverse cp1252: char -> byte, incluyendo los bytes indefinidos como C1
REV = {}
for b in range(0x80, 0x100):
    try:
        ch = bytes([b]).decode("cp1252")
    except UnicodeDecodeError:
        ch = chr(b)
    REV.setdefault(ch, b)

def encode_sloppy(run):
    out = bytearray()
    for ch in run:
        if ord(ch) <= 0xFF:
            out.append(ord(ch))
        elif ch in REV:
            out.append(REV[ch])
        else:
            return None
    return bytes(out)

def fix_run(run):
    b = encode_sloppy(run)
    if b is None:
        return run
    try:
        return b.decode("utf-8")
    except UnicodeDecodeError:
        return run

def fix(t, depth=4):
    for _ in range(depth):
        new = RUN.sub(lambda m: fix_run(m.group(0)), t)
        if new == t:
            break
        t = new
    return t

files = []
for dp, dn, fn in os.walk(root):
    for f in fn:
        if f.endswith(".md"):
            p = os.path.join(dp, f)
            t = open(p, "rb").read().decode("utf-8-sig")
            if RUN.search(t):
                files.append((p, t))

remaining = 0
for p, t in files:
    fixed = fix(t)
    left = len(RUN.findall(fixed))
    if left:
        remaining += 1
        print("RESTAN", left, p)
        for m in RUN.finditer(fixed):
            print("   ", ascii(m.group(0)))
    if p.endswith(r"gardener\SKILL.md"):
        print("OK gardener:", ascii(fixed.splitlines()[6])[:100])
print("archivos:", len(files), "con restos:", remaining)
