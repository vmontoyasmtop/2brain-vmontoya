import os, hashlib, collections
root = r"C:\Users\vmont\OneDrive\Desktop\2brain-vmontoya\.agents"
h = collections.defaultdict(list)
for dp, dn, fn in os.walk(root):
    for f in fn:
        p = os.path.join(dp, f)
        h[hashlib.sha256(open(p,"rb").read()).hexdigest()].append(p.replace(root+os.sep,""))
groups = [v for v in h.values() if len(v) > 1]
print("grupos:", len(groups), "archivos:", sum(len(g) for g in groups))
other = [g for g in groups if not any(x.startswith("agents\\") for x in g)]
print("grupos que NO son agents<->skills:", len(other))
for g in other[:10]:
    print("  ", g)
