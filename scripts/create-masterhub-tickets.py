#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI Oficial de Creación y Gestión de Tickets en MasterHub Helpdesk (Aiven Cloud DB)
===================================================================================
Autor: ALFRED (2brain System)
Propósito: Conectar a la base de datos de PostgreSQL en Aiven Cloud (helpdesk_db) e 
           insertar o listar tickets de soporte técnico de forma estandarizada sin 
           necesidad de crear scripts temporales.

Requisitos:
    pip install psycopg2-binary

Uso:
  1. Crear Ticket de Creación de Usuario (Shortcut):
     python scripts/create-masterhub-tickets.py --user-creation --name "Mileidy Yosmery Gonzalez Monsalve" --ci "32348627" --cargo "Cajera" --site "Beijing Naranjos"

  2. Crear Ticket Genérico (Incidencia o Requerimiento):
     python scripts/create-masterhub-tickets.py --title "[Barquisimeto] Falla de POS" --desc "Terminal de punto de venta no sincroniza" --site "Barquisimeto" --priority HIGH --type INCIDENT

  3. Listar Tickets Abiertos:
     python scripts/create-masterhub-tickets.py --list
"""

import os
import sys
import uuid
import re
import argparse
import json
import psycopg2

# Asegurar codificación UTF-8 en salida de terminal para Windows/Linux
if sys.platform == "win32":
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')

def load_env_file(filepath):
    """Carga variables clave de un archivo .env si existe."""
    if not os.path.exists(filepath):
        return {}
    env_vars = {}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env_vars[k.strip()] = v.strip().strip('"').strip("'")
    except Exception:
        pass
    return env_vars

def sanitize_dsn(uri):
    """Limpia y ajusta parámetros de consulta incompatibles con psycopg2 (ej: rejectUnauthorized, sslmode=no-verify)."""
    uri = uri.replace("sslmode=no-verify", "sslmode=require")
    if "?" in uri:
        base, query = uri.split("?", 1)
        params = query.split("&")
        valid_keys = {"sslmode", "connect_timeout", "application_name", "keepalives", "target_session_attrs", "sslcert", "sslkey", "sslrootcert"}
        valid_params = [p for p in params if p.split("=")[0] in valid_keys]
        if valid_params:
            return f"{base}?{'&'.join(valid_params)}"
        return base
    return uri

def get_database_url():
    """Obtiene la URL de conexión de helpdesk_db sin exponer credenciales hardcodeadas en Git."""
    # 1. Variables de entorno globales del sistema
    for env_key in ["HELPDESK_DB_URL", "DATABASE_URL"]:
        val = os.environ.get(env_key)
        if val and ("helpdesk_db" in val or "pg-masterhub" in val):
            return sanitize_dsn(val)

    # 2. Archivos .env locales (en 2brain/scripts/ o MasterHub/helpdesk-sm/)
    possible_envs = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env.local"),
        os.path.join(os.path.expanduser("~"), "Desktop", "MasterHub", "helpdesk-sm", ".env")
    ]

    for env_path in possible_envs:
        vars_dict = load_env_file(env_path)
        for key in ["HELPDESK_DB_URL", "DATABASE_URL"]:
            if key in vars_dict:
                val = vars_dict[key]
                if "helpdesk_db" in val or "pg-masterhub" in val:
                    return sanitize_dsn(val)

    print("❌ Error: No se encontró una cadena de conexión válida (HELPDESK_DB_URL o DATABASE_URL).")
    print("Asegúrate de tener configurado tu archivo scripts/.env o Desktop/MasterHub/helpdesk-sm/.env")
    sys.exit(1)

def generate_cuid():
    """Genera un identificador único tipo cuid para Prisma."""
    return f"cm{uuid.uuid4().hex[:22]}"

def slugify(text):
    """Convierte un texto en slug seguro para IDs."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '_', text).strip('_')
    return text

def connect_db():
    uri = get_database_url()
    try:
        conn = psycopg2.connect(uri)
        return conn
    except Exception as e:
        print(f"❌ Error al conectar con Aiven Cloud Database: {e}")
        sys.exit(1)

def list_tickets(limit=10, status_filter=None):
    """Muestra una lista resumida de tickets recientes."""
    conn = connect_db()
    cursor = conn.cursor()
    
    query = """
    SELECT "id", "title", "status", "priority", "siteName", "createdAt"
    FROM tickets
    """
    params = []
    if status_filter:
        query += ' WHERE "status" = %s'
        params.append(status_filter.upper())
        
    query += ' ORDER BY "createdAt" DESC LIMIT %s;'
    params.append(limit)
    
    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    
    print(f"\n📋 === ÚLTIMOS {len(rows)} TICKETS EN HELPDESK DB ===")
    print(f"{'ID':<26} | {'ESTADO':<10} | {'PRIORIDAD':<8} | {'SEDE':<20} | {'TÍTULO'}")
    print("-" * 95)
    for r in rows:
        tid, title, status, priority, site, created = r
        site_str = (site[:18] + '..') if site and len(site) > 20 else (site or 'N/A')
        title_str = (title[:30] + '..') if len(title) > 32 else title
        print(f"{tid:<26} | {status:<10} | {priority:<8} | {site_str:<20} | {title_str}")
        
    cursor.close()
    conn.close()

def create_ticket(data):
    """Inserta un nuevo ticket en la base de datos."""
    conn = connect_db()
    cursor = conn.cursor()

    ticket_id = data.get("id") or generate_cuid()
    site_name = data.get("siteName", "Sede Principal MasterGroup")
    site_id = data.get("siteId") or f"site_{slugify(site_name)}"

    query = """
    INSERT INTO tickets (
        "id", "title", "description", "type", "source", "status", "priority", "urgency", "importance",
        "siteId", "siteName", "requesterUserId", "requesterName", "assigneeName", "assigneeEmail",
        "createdAt", "updatedAt"
    ) VALUES (
        %s, %s, %s, 
        %s::"TicketType", %s::"TicketSource", %s::"TicketStatus", %s::"TicketPriority", 
        %s::"EisenhowerLevel", %s::"EisenhowerLevel", 
        %s, %s, %s, %s, %s, %s, NOW(), NOW()
    )
    RETURNING "id", "title", "status", "priority", "siteName", "createdAt";
    """

    cursor.execute(query, (
        ticket_id,
        data["title"],
        data.get("description", ""),
        data.get("type", "REQUEST"),
        data.get("source", "WALK_IN"),
        data.get("status", "OPEN"),
        data.get("priority", "MEDIUM"),
        data.get("urgency", "HIGH" if data.get("priority") in ["HIGH", "CRITICAL"] else "LOW"),
        data.get("importance", "HIGH"),
        site_id,
        site_name,
        data.get("requesterUserId", f"user_{slugify(data.get('requesterName', 'walkin'))}"),
        data.get("requesterName", "Solicitante Directo"),
        data.get("assigneeName", "Víctor Montoya"),
        data.get("assigneeEmail", "soporte@mastergroupve.com")
    ))

    row = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    result = {
        "id": row[0],
        "title": row[1],
        "status": row[2],
        "priority": row[3],
        "siteName": row[4],
        "createdAt": str(row[5])
    }

    print("\n✅ === TICKET REGISTRADO CON ÉXITO EN AIVEN CLOUD ===")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return result

def main():
    parser = argparse.ArgumentParser(description="CLI Estandarizado de Creación de Tickets para MasterHub Helpdesk")
    
    # Atajos especiales
    parser.add_argument("--user-creation", "--crear-usuario", action="store_true", help="Crear ticket preformateado de Creación de Usuario")
    parser.add_argument("--name", "--nombre", type=str, help="Nombre completo del empleado (para --user-creation o requester)")
    parser.add_argument("--ci", type=str, help="Cédula de identidad del empleado")
    parser.add_argument("--cargo", type=str, help="Cargo del empleado (ej: Cajera, Subgerente)")
    
    # Campos genéricos
    parser.add_argument("--title", "--titulo", type=str, help="Título del ticket")
    parser.add_argument("--desc", "--description", type=str, help="Descripción detallada de la incidencia/requerimiento")
    parser.add_argument("--site", "--sede", type=str, default="Principal", help="Nombre de la sede/sucursal (ej: Beijing Naranjos, Barquisimeto)")
    parser.add_argument("--type", type=str, choices=["INCIDENT", "REQUEST"], default=None, help="Tipo de ticket")
    parser.add_argument("--priority", type=str, choices=["LOW", "MEDIUM", "HIGH", "CRITICAL"], default="MEDIUM", help="Prioridad")
    parser.add_argument("--source", type=str, choices=["WALK_IN", "PHONE", "EMAIL", "WEB"], default="WALK_IN", help="Origen del reporte")
    parser.add_argument("--status", type=str, choices=["OPEN", "IN_PROGRESS", "RESOLVED", "CLOSED"], default="OPEN", help="Estado inicial")
    parser.add_argument("--requester", type=str, help="Nombre del solicitante")

    # Acciones
    parser.add_argument("--list", action="store_true", help="Listar últimos tickets creados")
    parser.add_argument("--limit", type=int, default=10, help="Límite de tickets a listar")

    args = parser.parse_args()

    if args.list:
        list_tickets(limit=args.limit, status_filter=args.status if args.status != "OPEN" else None)
        return

    # Modo 1: Creación de Usuario Shortcut
    if args.user_creation:
        if not args.name or not args.ci:
            print("❌ Error: Para --user-creation debes especificar --name y --ci (y opcionalmente --cargo y --site).")
            sys.exit(1)
            
        cargo_str = f" ({args.cargo})" if args.cargo else ""
        site_str = args.site if args.site.lower().startswith("sede") else f"Sede {args.site}"
        
        ticket_data = {
            "title": f"[{args.site}] Creación de Usuario - {args.name}{cargo_str}",
            "description": f"Requerimiento de creación de usuario para nuevo ingreso en {site_str}.\n\nDatos de la empleada:\n- Nombre Completo: {args.name}\n- C.I.: {args.ci}\n- Cargo: {args.cargo or 'N/A'}\n- Sede: {site_str}",
            "type": "REQUEST",
            "source": args.source,
            "status": args.status,
            "priority": args.priority,
            "siteName": site_str,
            "siteId": f"site_{slugify(args.site)}",
            "requesterUserId": f"user_{slugify(args.name)}",
            "requesterName": f"{args.name} (C.I. {args.ci}{cargo_str})"
        }
        create_ticket(ticket_data)
        return

    # Modo 2: Ticket Genérico
    if args.title:
        site_str = args.site if args.site.lower().startswith("sede") else f"Sede {args.site}"
        ticket_type = args.type or ("REQUEST" if "creacion" in args.title.lower() or "usuario" in args.title.lower() else "INCIDENT")
        
        ticket_data = {
            "title": args.title if args.title.startswith("[") else f"[{args.site}] {args.title}",
            "description": args.desc or args.title,
            "type": ticket_type,
            "source": args.source,
            "status": args.status,
            "priority": args.priority,
            "siteName": site_str,
            "siteId": f"site_{slugify(args.site)}",
            "requesterName": args.requester or args.name or "Solicitante Directo"
        }
        create_ticket(ticket_data)
        return

    # Si no se pasaron argumentos válidos, mostrar ayuda y listar tickets
    parser.print_help()
    print("\nEjemplo de ejecución rápida para crear usuario:")
    print('  python scripts/create-masterhub-tickets.py --user-creation --name "Juan Perez" --ci "12345678" --cargo "Cajero" --site "Beijing Naranjos"\n')

if __name__ == "__main__":
    main()
