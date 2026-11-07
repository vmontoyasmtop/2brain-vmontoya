#!/usr/bin/env python3
"""Auditoría del sistema de agentes de 2brain.

Comprueba:
  1. Codificación UTF-8 estricta en AGENTS.md, .agents/ y agents/.
  2. Frontmatter obligatorio (name, description) y name == carpeta.
  3. Duplicados exactos (SHA-256) dentro de .agents/.
  4. Rutas absolutas muertas y herramientas inexistentes en las especificaciones.
  5. Roles de los manifiestos de pack que no existen como skill.

Uso:
    python scripts/audit_agents.py
    python scripts/audit_agents.py --json
    python scripts/audit_agents.py --strict   # los warnings también fallan
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = ROOT / ".agents"
SKILLS_DIR = AGENTS_DIR / "skills"
PACKS_DIR = AGENTS_DIR / "packs"
LEGACY_DIR = ROOT / "agents"

# Solo se revisan las especificaciones, no la documentación de arquitectura.
SPEC_GLOBS = [
    AGENTS_DIR / "skills" / "*" / "SKILL.md",
    AGENTS_DIR / "agents" / "*.md",
    AGENTS_DIR / "rules" / "*.md",
    LEGACY_DIR / "*.md",
    ROOT / "AGENTS.md",
]

FORBIDDEN_TOKENS = [
    "invoke_subagent",
    "define_subagent",
    "C:\\Users\\vmontoyaMG",
    "2brain-MG",
]

PACK_NAMES = {"core", "akatsuki", "fellowship"}

# Secuencias típicas de texto UTF-8 leído como cp1252 y vuelto a guardar.
MOJIBAKE_RE = re.compile(r"[\u00c3\u00c2]|\u00e2\u20ac|\u00f0\u0178")

findings: list[dict] = []


def add(level: str, check: str, path: Path | str, message: str) -> None:
    findings.append(
        {
            "level": level,
            "check": check,
            "path": str(path).replace(str(ROOT) + "\\", "").replace("\\", "/"),
            "message": message,
        }
    )


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end]
    data: dict[str, str] = {}
    for line in block.splitlines():
        m = re.match(r"^([a-zA-Z_][\w-]*):\s*(.*)$", line)
        if m:
            data[m.group(1)] = m.group(2).strip()
    return data


def check_encoding(path: Path) -> None:
    try:
        path.read_bytes().decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        add("error", "encoding", path, f"no es UTF-8 valido: {exc}")


def safe_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        return None


def check_mojibake(path: Path) -> None:
    text = safe_text(path)
    if text is None:
        return
    count = len(MOJIBAKE_RE.findall(text))
    if count:
        add("error", "mojibake", path, f"{count} secuencias corruptas (doble codificacion UTF-8)")


def check_skill(skill: Path) -> None:
    text = safe_text(skill)
    if text is None:
        return  # ya reportado por check_encoding
    fm = parse_frontmatter(text)
    if not fm:
        add("error", "frontmatter", skill, "sin frontmatter")
        return
    for key in ("name", "description"):
        if not fm.get(key):
            add("error", "frontmatter", skill, f"falta '{key}'")
    name = fm.get("name", "").strip().strip('"').strip("'")
    if name and name != skill.parent.name:
        add("error", "frontmatter", skill, f"name='{name}' != carpeta '{skill.parent.name}'")
    pack = fm.get("pack", "").strip().strip('"').strip("'")
    if pack and pack not in PACK_NAMES:
        add("warning", "pack", skill, f"pack desconocido '{pack}'")


def check_duplicates() -> None:
    by_hash: dict[str, list[Path]] = defaultdict(list)
    for path in AGENTS_DIR.rglob("*.md"):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        by_hash[digest].append(path)
    for digest, paths in by_hash.items():
        if len(paths) > 1:
            rel = ", ".join(
                str(p).replace(str(ROOT) + "\\", "").replace("\\", "/") for p in paths
            )
            add("warning", "duplicado", paths[0], f"{len(paths)} copias identicas: {rel}")


def check_forbidden() -> None:
    for pattern in SPEC_GLOBS:
        for path in ROOT.glob(str(pattern.relative_to(ROOT))):
            text = safe_text(path)
            if text is None:
                continue
            hits = [token for token in FORBIDDEN_TOKENS if token in text]
            if hits:
                add("error", "ruta/tool", path, "contiene: " + ", ".join(hits))


def check_pack_roles() -> None:
    for pack in sorted(PACKS_DIR.glob("*.yaml")):
        text = safe_text(pack) or ""
        slugs: set[str] = set()
        in_roles = False
        for line in text.splitlines():
            if re.match(r"^roles:\s*$", line):
                in_roles = True
                continue
            if in_roles and re.match(r"^\S", line):
                in_roles = False
            if in_roles:
                m = re.match(r"^\s+[a-z_]+:\s*([a-z0-9-]+)\s*$", line)
                if m:
                    slugs.add(m.group(1))
        for slug in sorted(slugs):
            if not (SKILLS_DIR / slug / "SKILL.md").exists():
                add("error", "pack", pack, f"rol '{slug}' sin skill en .agents/skills/")


def main() -> int:
    parser = argparse.ArgumentParser(description="Audita el sistema de agentes 2brain")
    parser.add_argument("--json", action="store_true", help="salida JSON")
    parser.add_argument("--strict", action="store_true", help="warnings también fallan")
    args = parser.parse_args()

    for pattern in SPEC_GLOBS:
        for path in ROOT.glob(str(pattern.relative_to(ROOT))):
            check_encoding(path)
            check_mojibake(path)

    for skill in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        check_skill(skill)

    check_duplicates()
    check_forbidden()
    check_pack_roles()

    errors = [f for f in findings if f["level"] == "error"]
    warnings = [f for f in findings if f["level"] == "warning"]

    if args.json:
        print(json.dumps({"errors": errors, "warnings": warnings}, ensure_ascii=False, indent=2))
    else:
        for level, title in (("error", "ERRORES"), ("warning", "ADVERTENCIAS")):
            items = [f for f in findings if f["level"] == level]
            print(f"\n{title}: {len(items)}")
            for item in items[:60]:
                print(f"  [{item['check']}] {item['path']}: {item['message']}")
            if len(items) > 60:
                print(f"  ... y {len(items) - 60} más")
        print(f"\nResumen: {len(errors)} errores, {len(warnings)} advertencias")

    if errors:
        return 1
    if args.strict and warnings:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
