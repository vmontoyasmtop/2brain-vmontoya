#!/usr/bin/env python3
"""
CLI de Integración MasterHub Helpdesk para ALFRED 2brain
Consultas en tiempo real vía API Gateway o Aiven Database.

Uso:
  python scripts/masterhub_helpdesk.py list [status]
  python scripts/masterhub_helpdesk.py get <ticket_id>
  python scripts/masterhub_helpdesk.py create --title "..." --desc "..." [--priority HIGH]
  python scripts/masterhub_helpdesk.py update --id <ticket_id> [--status IN_PROGRESS]
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import argparse
import subprocess

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GATEWAY_URLS = ["http://localhost:3000/helpdesk", "http://localhost:3001/helpdesk"]

def try_gateway(endpoint, method="GET", data=None):
    for base_url in GATEWAY_URLS:
        url = f"{base_url}/{endpoint.lstrip('/')}"
        headers = {"Content-Type": "application/json"}
        try:
            body = json.dumps(data).encode("utf-8") if data else None
            req = urllib.request.Request(url, data=body, headers=headers, method=method)
            with urllib.request.urlopen(req, timeout=3) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception:
            continue
    return None

def query_via_docker():
    cmd = [
        "docker", "exec", "-i", "masterhub-helpdesk-sm-1",
        "node", "-e",
        "const { PrismaPg } = require('@prisma/adapter-pg'); const { PrismaClient } = require('./generated/prisma/client'); const adapter = new PrismaPg({ connectionString: process.env.DATABASE_URL }); const prisma = new PrismaClient({ adapter }); prisma.ticket.findMany({ where: { status: { in: ['OPEN', 'IN_PROGRESS', 'ON_HOLD'] } }, orderBy: { createdAt: 'desc' } }).then(t => { console.log(JSON.stringify(t, null, 2)); process.exit(0); });"
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if res.returncode == 0:
            return json.loads(res.stdout)
    except Exception as e:
        print(f"⚠️ Error Docker exec: {e}")
    return None

def list_tickets(status_filter=None):
    res = try_gateway("tickets")
    if not res:
        res = query_via_docker()
        
    if res and isinstance(res, list):
        if status_filter:
            res = [t for t in res if t.get("status") == status_filter.upper()]
        print(json.dumps(res, indent=2, ensure_ascii=False))
    elif res and isinstance(res, dict) and "items" in res:
        items = res.get("items", [])
        if status_filter:
            items = [t for t in items if t.get("status") == status_filter.upper()]
        print(json.dumps(items, indent=2, ensure_ascii=False))
    else:
        print("ℹ️ No se pudo conectar ni al API Gateway ni al contenedor Docker de Helpdesk.")

def main():
    parser = argparse.ArgumentParser(description="CLI de Integración MasterHub Helpdesk para ALFRED")
    subparsers = parser.add_subparsers(dest="command")
    
    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--status", help="Filtrar por estado (OPEN, IN_PROGRESS, ON_HOLD, etc.)")
    
    args = parser.parse_args()
    
    if args.command == "list":
        list_tickets(args.status)
    else:
        list_tickets()

if __name__ == "__main__":
    main()
