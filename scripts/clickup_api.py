#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ClickUp API Client & CLI para ALFRED y Pain (Akatsuki Suite)
============================================================
Autor: ALFRED (2brain System)
Propósito: Permitir a Pain y a los subagentes consultar, crear y actualizar
           proyectos, listas, tareas y subtareas en ClickUp de forma programática.
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import urllib.error
import argparse
from typing import Dict, Any, Optional

if sys.platform == "win32":
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_LOCAL = os.path.join(BASE_DIR, "scripts", ".env.local")
ENV_DEFAULT = os.path.join(BASE_DIR, "scripts", ".env")

def load_env() -> Dict[str, str]:
    config = {}
    for path in [ENV_DEFAULT, ENV_LOCAL]:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        config[k.strip()] = v.strip()
    return config

ENV_CONFIG = load_env()
TOKEN = os.environ.get("CLICKUP_API_TOKEN") or ENV_CONFIG.get("CLICKUP_API_TOKEN") or ENV_CONFIG.get("CLICKUP_PERSONAL_TOKEN")
API_BASE = "https://api.clickup.com/api/v2"

def clickup_request(endpoint: str, method: str = "GET", data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    if not TOKEN:
        raise ValueError("Token de ClickUp no encontrado en .env o entorno.")
    
    url = f"{API_BASE}{endpoint}"
    headers = {
        "Authorization": TOKEN,
        "Content-Type": "application/json"
    }
    
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode("utf-8")
            return json.loads(content) if content else {}
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        print(f"❌ Error ClickUp API ({e.code}): {err_msg}", file=sys.stderr)
        raise e

def get_user() -> Dict[str, Any]:
    return clickup_request("/user")

def get_teams() -> Dict[str, Any]:
    return clickup_request("/team")

def get_spaces(team_id: str) -> Dict[str, Any]:
    return clickup_request(f"/team/{team_id}/space")

def get_lists(folder_or_space_id: str, is_space: bool = False) -> Dict[str, Any]:
    if is_space:
        return clickup_request(f"/space/{folder_or_space_id}/list")
    return clickup_request(f"/folder/{folder_or_space_id}/list")

def create_task(list_id: str, name: str, description: str = "", priority: int = 3, tags: list = None, parent: str = None, start_date: int = None, due_date: int = None) -> Dict[str, Any]:
    payload = {
        "name": name,
        "markdown_description": description,
        "priority": priority,
    }
    if tags:
        payload["tags"] = tags
    if parent:
        payload["parent"] = parent
    if start_date:
        payload["start_date"] = start_date
        payload["start_date_time"] = True
    if due_date:
        payload["due_date"] = due_date
        payload["due_date_time"] = True
        
    return clickup_request(f"/list/{list_id}/task", method="POST", data=payload)

def get_tasks(list_id: str) -> Dict[str, Any]:
    return clickup_request(f"/list/{list_id}/task?include_closed=true&subtasks=true")

def update_task_status(task_id: str, status: str) -> Dict[str, Any]:
    return clickup_request(f"/task/{task_id}", method="PUT", data={"status": status})

def main():
    parser = argparse.ArgumentParser(description="ClickUp CLI para ALFRED & Akatsuki")
    parser.add_argument("--whoami", action="store_true", help="Comprobar credencial y usuario de ClickUp")
    parser.add_argument("--teams", action="store_true", help="Listar equipos/workspaces de ClickUp")
    parser.add_argument("--spaces", type=str, help="Listar espacios del equipo especificado (team_id)")
    parser.add_argument("--lists", type=str, help="Listar listas del espacio especificado (space_id)")
    parser.add_argument("--tasks", type=str, help="Listar tareas de una lista (list_id)")
    parser.add_argument("--update-status", nargs=2, metavar=("TASK_ID", "STATUS"), help="Actualizar estado de una tarea")
    parser.add_argument("--create-task", type=str, help="ID de la lista donde crear la tarea")
    parser.add_argument("--name", type=str, help="Nombre de la tarea")
    parser.add_argument("--desc", type=str, default="", help="Descripción en Markdown de la tarea")
    parser.add_argument("--priority", type=int, default=3, help="Prioridad (1=Urgente, 2=Alta, 3=Normal, 4=Baja)")
    parser.add_argument("--tags", type=str, default="", help="Tags separados por coma")
    parser.add_argument("--parent", type=str, help="ID de la tarea padre (si es subtarea)")
    
    args = parser.parse_args()
    
    try:
        if args.whoami:
            u = get_user()
            print(f"✅ Conectado a ClickUp como: {u['user']['username']} ({u['user']['email']})")
        elif args.teams:
            teams = get_teams()
            print(json.dumps(teams, indent=2, ensure_ascii=False))
        elif args.spaces:
            spaces = get_spaces(args.spaces)
            print(json.dumps(spaces, indent=2, ensure_ascii=False))
        elif args.lists:
            lists = get_lists(args.lists, is_space=True)
            print(json.dumps(lists, indent=2, ensure_ascii=False))
        elif args.tasks:
            tasks = get_tasks(args.tasks)
            print(json.dumps(tasks, indent=2, ensure_ascii=False))
        elif args.update_status:
            t = update_task_status(args.update_status[0], args.update_status[1])
            print(f"✅ Tarea {args.update_status[0]} actualizada al estado '{args.update_status[1]}'")
        elif args.create_task and args.name:
            tag_list = [t.strip() for t in args.tags.split(",") if t.strip()]
            t = create_task(args.create_task, args.name, args.desc, args.priority, tag_list, args.parent)
            print(f"✅ Tarea creada exitosamente: ID={t.get('id')} - URL={t.get('url')}")
        else:
            parser.print_help()
    except Exception as e:
        print(f"❌ Error en ClickUp API: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
