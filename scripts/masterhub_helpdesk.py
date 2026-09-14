#!/usr/bin/env python3
"""
CLI de Integración MasterHub Helpdesk para ALFRED 2brain
Permite a ALFRED consultar, crear y actualizar tickets de Helpdesk.

Uso:
  python scripts/masterhub_helpdesk.py list [status]
  python scripts/masterhub_helpdesk.py get <ticket_id>
  python scripts/masterhub_helpdesk.py create --title "..." --desc "..." [--priority HIGH] [--type INCIDENT]
  python scripts/masterhub_helpdesk.py update --id <ticket_id> [--status IN_PROGRESS] [--notes "..."]
  python scripts/masterhub_helpdesk.py eisenhower
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import argparse

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GATEWAY_URL = os.environ.get("MASTERHUB_GATEWAY_URL", "http://localhost:3000/helpdesk")
JWT_TOKEN = os.environ.get("MASTERHUB_JWT_TOKEN", "")

def make_request(endpoint, method="GET", data=None):
    url = f"{GATEWAY_URL}/{endpoint.lstrip('/')}"
    headers = {"Content-Type": "application/json"}
    if JWT_TOKEN:
        headers["Authorization"] = f"Bearer {JWT_TOKEN}"
        
    try:
        body = json.dumps(data).encode("utf-8") if data else None
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as e:
        print(f"⚠️ Error al conectar con MasterHub Gateway ({url}): {e}")
        return None
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return None

def list_tickets(status=None):
    endpoint = "tickets"
    if status:
        endpoint += f"?status={urllib.parse.quote(status)}"
    res = make_request(endpoint)
    if res:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print("ℹ️ No se pudo conectar al API Gateway de MasterHub (Asegúrese de que npm run start:all o Docker esté corriendo).")

def get_ticket(ticket_id):
    res = make_request(f"tickets/{ticket_id}")
    if res:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print(f"ℹ️ No se encontró el ticket '{ticket_id}' o el servidor no está activo.")

def create_ticket(title, description, priority="MEDIUM", type_ticket="INCIDENT", site_name="Sede Principal"):
    payload = {
        "title": title,
        "description": description,
        "priority": priority,
        "type": type_ticket,
        "siteId": "site_default",
        "siteName": site_name,
        "requesterUserId": "alfred_bot",
        "requesterName": "ALFRED (2brain Assistant)"
    }
    res = make_request("tickets", method="POST", data=payload)
    if res:
        print("✅ Ticket creado exitosamente:")
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print("ℹ️ No se pudo registrar el ticket. Verifique que MasterHub API Gateway esté activo en http://localhost:3000.")

def update_ticket(ticket_id, status=None, notes=None, assignee_name=None):
    payload = {}
    if status:
        payload["status"] = status
    if notes:
        payload["resolutionNotes"] = notes
    if assignee_name:
        payload["assigneeName"] = assignee_name
        
    res = make_request(f"tickets/{ticket_id}", method="PATCH", data=payload)
    if res:
        print(f"✅ Ticket '{ticket_id}' actualizado:")
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print(f"ℹ️ No se pudo actualizar el ticket '{ticket_id}'.")

def get_eisenhower():
    res = make_request("tickets/eisenhower")
    if res:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print("ℹ️ Matriz de Eisenhower no disponible temporalmente.")

def main():
    parser = argparse.ArgumentParser(description="CLI de Integración MasterHub Helpdesk para ALFRED")
    subparsers = parser.add_subparsers(dest="command")
    
    # List
    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--status", help="Filtrar por estado (OPEN, IN_PROGRESS, RESOLVED, etc.)")
    
    # Get
    get_parser = subparsers.add_parser("get")
    get_parser.add_argument("id", help="ID del ticket")
    
    # Create
    create_parser = subparsers.add_parser("create")
    create_parser.add_argument("--title", required=True, help="Título del ticket")
    create_parser.add_argument("--desc", required=True, help="Descripción")
    create_parser.add_argument("--priority", default="MEDIUM", choices=["LOW", "MEDIUM", "HIGH", "CRITICAL"])
    create_parser.add_argument("--type", default="INCIDENT", choices=["INCIDENT", "REQUEST"])
    
    # Update
    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("--id", required=True, help="ID del ticket")
    update_parser.add_argument("--status", choices=["OPEN", "IN_PROGRESS", "ON_HOLD", "RESOLVED", "CLOSED", "CANCELLED"])
    update_parser.add_argument("--notes", help="Notas de solución")
    
    # Eisenhower
    subparsers.add_parser("eisenhower")
    
    args = parser.parse_args()
    
    if args.command == "list":
        list_tickets(args.status)
    elif args.command == "get":
        get_ticket(args.id)
    elif args.command == "create":
        create_ticket(args.title, args.desc, args.priority, args.type)
    elif args.command == "update":
        update_ticket(args.id, args.status, args.notes)
    elif args.command == "eisenhower":
        get_eisenhower()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
