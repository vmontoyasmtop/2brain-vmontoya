import os
import sys
import argparse
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "raw"
WIKI_DIR = BASE_DIR / "wiki"

AREAS = ["trabajo", "programacion", "proyectos", "ministerial", "familiar", "finanzas"]

def cmd_status():
    raw_sources = [f for f in RAW_DIR.rglob("*.*") if f.is_file() and not f.name.startswith(".")] if RAW_DIR.exists() else []
    all_wiki_md = list(WIKI_DIR.rglob("*.md")) if WIKI_DIR.exists() else []
    
    summaries = [f for f in all_wiki_md if "summaries" in f.parts]
    concepts = [f for f in all_wiki_md if "concepts" in f.parts]
    entities = [f for f in all_wiki_md if "entities" in f.parts]

    print("[2brain] Status Report")
    print("=" * 40)
    print(f"Total fuentes en raw/:     {len(raw_sources)}")
    print(f"Total notas en wiki/:      {len(all_wiki_md)}")
    print(f"  - Resúmenes (summaries): {len(summaries)}")
    print(f"  - Conceptos (concepts):  {len(concepts)}")
    print(f"  - Entidades (entities):  {len(entities)}")
    print("=" * 40)
    print("Desglose por Áreas:")
    for area in AREAS:
        raw_area = [f for f in raw_sources if area in f.parts]
        wiki_area = [f for f in all_wiki_md if area in f.parts or f.name.lower().startswith(f"pilar-{area}")]
        print(f"  📌 {area.capitalize():<14} | raw: {len(raw_area):<3} | wiki: {len(wiki_area):<3}")
    print("=" * 40)

def cmd_search(query):
    print(f"Buscando '{query}' en 2brain wiki...")
    print("-" * 45)
    matches = 0
    query_lower = query.lower()

    for root, _, files in os.walk(WIKI_DIR):
        for file in files:
            if file.endswith(".md"):
                filepath = Path(root) / file
                try:
                    content = filepath.read_text(encoding="utf-8")
                    if query_lower in content.lower():
                        rel_path = filepath.relative_to(BASE_DIR)
                        print(f"Coincidencia en: {rel_path}")
                        matches += 1
                except Exception:
                    pass
    if matches == 0:
        print("No se encontraron coincidencias.")

def cmd_pending():
    print("Verificando fuentes en raw/ vs resúmenes procesados...")
    raw_sources = [f for f in RAW_DIR.rglob("*.*") if f.is_file() and not f.name.startswith(".")]
    summaries = [f.stem for f in WIKI_DIR.rglob("*.md") if "summaries" in f.parts]

    pending = []
    for source in raw_sources:
        if source.stem not in summaries and f"{source.stem}-gist" not in summaries:
            rel = source.relative_to(BASE_DIR)
            pending.append(str(rel))

    if pending:
        print(f"Hay {len(pending)} fuente(s) potencialmente pendiente(s) de ingestión:")
        for p in pending:
            print(f"  - {p}")
    else:
        print("Todas las fuentes en raw/ han sido procesadas.")

def main():
    parser = argparse.ArgumentParser(description="2brain CLI Helper")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("status", help="Muestra el estado de la wiki por áreas")
    subparsers.add_parser("pending", help="Muestra fuentes pendientes en raw/")
    search_parser = subparsers.add_parser("search", help="Busca un término en la wiki")
    search_parser.add_argument("query", type=str, help="Término a buscar")

    args = parser.parse_args()

    if args.command == "status":
        cmd_status()
    elif args.command == "pending":
        cmd_pending()
    elif args.command == "search":
        cmd_search(args.query)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
