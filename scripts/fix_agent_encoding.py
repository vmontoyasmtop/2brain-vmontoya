#!/usr/bin/env python3
"""Repara el mojibake de .agents/ (UTF-8 leido como cp1252 y vuelto a guardar).

Uso:
    python scripts/fix_agent_encoding.py --dry-run
    python scripts/fix_agent_encoding.py --apply
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / ".agents"

LEAD = "\u00c3\u00c2\u00f0\u00e2"
TAIL = (
    "\u0080-\u00ff\u0152\u0153\u0160\u0161\u0178\u017d\u017e\u0192\u02c6\u02dc"
    "\u2013\u2014\u2018\u2019\u201a\u201c\u201d\u201e\u2020\u2021\u2022\u2026"
    "\u2030\u2039\u203a\u20ac\u2122"
)
RUN = re.compile(f"[{LEAD}][{TAIL}]+")

# cp1252 inverso, incluyendo los bytes indefinidos como controles C1
REV: dict[str, int] = {}
for _b in range(0x80, 0x100):
    try:
        _ch = bytes([_b]).decode("cp1252")
    except UnicodeDecodeError:
        _ch = chr(_b)
    REV.setdefault(_ch, _b)


def encode_sloppy(run: str) -> bytes | None:
    out = bytearray()
    for ch in run:
        if ord(ch) <= 0xFF:
            out.append(ord(ch))
        elif ch in REV:
            out.append(REV[ch])
        else:
            return None
    return bytes(out)


def fix_run(run: str) -> str:
    raw = encode_sloppy(run)
    if raw is None:
        return run
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return run


def fix_text(text: str, depth: int = 4) -> str:
    for _ in range(depth):
        fixed = RUN.sub(lambda m: fix_run(m.group(0)), text)
        if fixed == text:
            break
        text = fixed
    return text


def read(path: Path) -> tuple[str, bool]:
    raw = path.read_bytes()
    return raw.decode("utf-8-sig"), raw.startswith(b"\xef\xbb\xbf")


def write(path: Path, text: str, bom: bool) -> None:
    path.write_bytes(text.encode("utf-8-sig" if bom else "utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if not args.apply and not args.dry_run:
        args.dry_run = True

    touched = 0
    for path in sorted(AGENTS.rglob("*.md")):
        text, bom = read(path)
        if not RUN.search(text):
            continue
        fixed = fix_text(text)
        remaining = len(RUN.findall(fixed))
        touched += 1
        if args.dry_run:
            print(f"{'OK ' if not remaining else 'REV'} {path.relative_to(ROOT)} ({remaining} restantes)")
        else:
            write(path, fixed, bom)
            print(f"fix {path.relative_to(ROOT)}")

    # La regla de ALFRED estaba truncada: se regenera desde el skill (fuente de verdad).
    rule = AGENTS / "rules" / "alfred.md"
    skill = AGENTS / "skills" / "alfred" / "SKILL.md"
    if skill.exists() and rule.exists():
        body = read(skill)[0]
        if body.startswith("---"):
            end = body.find("\n---", 3)
            body = body[end + 4 :].lstrip("\n")
        _, rule_bom = read(rule)
        if args.dry_run:
            print(f"OK  {rule.relative_to(ROOT)} (regenerar desde skill: {len(body)} chars)")
        else:
            write(rule, body, rule_bom)
            print(f"reg {rule.relative_to(ROOT)} ({len(body)} chars)")

    print(f"\nArchivos procesados: {touched}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
