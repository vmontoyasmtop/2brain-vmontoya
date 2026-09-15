#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Creación e Inserción Directa de Tickets en MasterHub Helpdesk (Aiven Cloud DB)
=======================================================================================
Autor: ALFRED (2brain System)
Propósito: Conectar a la base de datos de PostgreSQL en Aiven Cloud (helpdesk_db) e 
           insertar tickets de soporte técnico con clasificación de Matriz Eisenhower.

Requisitos:
    pip install psycopg2-binary

Uso:
    $env:DATABASE_URL="postgres://avnadmin:...@pg-masterhub-masterhub.j.aivencloud.com:28688/helpdesk_db?sslmode=require"
    python scripts/create-masterhub-tickets.py
"""

import os
import sys
import uuid
import psycopg2

# Asegurar codificación UTF-8 en salida de terminal para Windows/Linux
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# Obtener URI desde variable de entorno DATABASE_URL o prompt
DB_URI = os.environ.get("DATABASE_URL") or os.environ.get("HELPDESK_DB_URL")

def generate_cuid():
    """Genera un identificador único compatible con cuid/uuid para Prisma."""
    return f"cm{uuid.uuid4().hex[:20]}"

def create_tickets(tickets_list, db_uri=None):
    """
    Recibe una lista de diccionarios con datos de tickets e inserta cada uno en Aiven DB.
    """
    uri = db_uri or DB_URI
    if not uri:
        print("❌ Error: No se encontró la variable de entorno DATABASE_URL.")
        print("Ejemplo en PowerShell:")
        print('  $env:DATABASE_URL="postgres://user:password@host:port/helpdesk_db?sslmode=require"')
        sys.exit(1)

    print("🔌 Conectando a Aiven Cloud PostgreSQL (helpdesk_db)...")
    conn = psycopg2.connect(uri)
    cursor = conn.cursor()

    query = """
    INSERT INTO tickets (
        "id", "title", "description", "type", "source", "status", "priority", "urgency", "importance",
        "siteId", "siteName", "requesterUserId", "requesterName", "assigneeName", "assigneeEmail",
        "createdAt", "updatedAt"
    ) VALUES (%s, %s, %s, %s::"TicketType", %s::"TicketSource", %s::"TicketStatus", %s::"TicketPriority", %s::"EisenhowerLevel", %s::"EisenhowerLevel", %s, %s, %s, %s, %s, %s, NOW(), NOW())
    RETURNING "id", "title", "status", "priority";
    """

    created_records = []
    for t in tickets_list:
        ticket_id = t.get("id") or generate_cuid()
        cursor.execute(query, (
            ticket_id,
            t["title"],
            t.get("description", ""),
            t.get("type", "INCIDENT"),
            t.get("source", "WALK_IN"),
            t.get("status", "IN_PROGRESS"),
            t.get("priority", "MEDIUM"),
            t.get("urgency", "HIGH" if t.get("priority") in ["HIGH", "CRITICAL"] else "LOW"),
            t.get("importance", "HIGH"),
            t.get("siteId", "1"),
            t.get("siteName", "Sede Principal MasterGroup"),
            t.get("requesterUserId", "user_walkin"),
            t.get("requesterName", "Solicitante Directo"),
            t.get("assigneeName", "Víctor Montoya"),
            t.get("assigneeEmail", "soporte@mastergroupve.com")
        ))
        row = cursor.fetchone()
        created_records.append(row)
        print(f"✅ Ticket registrado: ID={row[0]} | Prioridad={row[3]} | Título='{row[1]}'")

    conn.commit()
    cursor.close()
    conn.close()
    print("\n🎉 ¡Inserción completada exitosamente en la base de datos de Aiven Cloud!")
    return created_records

if __name__ == "__main__":
    sample_tickets = [
        {
            "title": "Soporte Tailin: Bug de colores en laptop",
            "description": "Incidencia técnica: Corrección y ajuste de perfil de colores / controlador gráfico en la laptop de Tailin.",
            "type": "INCIDENT",
            "priority": "HIGH",
            "requesterName": "Tailin"
        }
    ]
    
    create_tickets(sample_tickets)
