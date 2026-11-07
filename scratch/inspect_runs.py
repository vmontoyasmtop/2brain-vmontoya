import os, re
root = r"C:\Users\vmont\OneDrive\Desktop\2brain-vmontoya\.agents"
LEAD = "\u00c3\u00c2\u00f0\u00e2"
TAIL = "\u0080-\u00ff\u0152\u0153\u0160\u0161\u0178\u017d\u017e\u0192\u02c6\u02dc\u2013\u2014\u2018\u2019\u201a\u201c\u201d\u201e\u2020\u2021\u2022\u2026\u2030\u2039\u203a\u20ac\u2122"
RUN = re.compile(f"[{LEAD}][{TAIL}]+")
for rel in [r"skills\backend-js\SKILL.md", r"skills\it-support\SKILL.md", r"skills\project-manager\SKILL.md", r"skills\synthesizer\SKILL.md"]:
    p = os.path.join(root, rel)
    t = open(p, "rb").read().decode("utf-8-sig")
    for m in RUN.finditer(t):
        s = max(0, m.start()-40); e = min(len(t), m.end()+40)
        print(rel, "=>", ascii(t[s:e]))
        print("   run:", [hex(ord(c)) for c in m.group(0)])
