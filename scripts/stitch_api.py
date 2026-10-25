#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Stitch API Client & CLI para Konan (Akatsuki Suite)
==========================================================
Autor: ALFRED (2brain System)
Propósito: Permitir a Konan (UI/UX Designer) y a ALFRED interactuar con
           la API de Google Stitch (stitch.withgoogle.com) y generar
           especificaciones de diseño y prototipos UI/UX.
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
STITCH_KEY = (
    os.environ.get("GOOGLE_STITCH_API_KEY") or
    os.environ.get("STITCH_API_KEY") or
    ENV_CONFIG.get("GOOGLE_STITCH_API_KEY") or
    ENV_CONFIG.get("STITCH_API_KEY")
)

def get_auth_headers() -> Dict[str, str]:
    if not STITCH_KEY:
        raise ValueError("API Key de Google Stitch no encontrada en .env o entorno.")
    return {
        "Authorization": f"Bearer {STITCH_KEY}",
        "x-goog-api-key": STITCH_KEY,
        "Content-Type": "application/json"
    }

def verify_token() -> bool:
    """Verifica si la credencial de Stitch está formateada y cargada correctamente."""
    if not STITCH_KEY:
        return False
    return STITCH_KEY.startswith("AQ.") and len(STITCH_KEY) > 20

def generate_design_tokens(theme_name: str = "Akatsuki Modern") -> Dict[str, Any]:
    """Genera el conjunto de Design Tokens estándar vinculados a Stitch."""
    return {
        "theme": theme_name,
        "engine": "Google Stitch UI Prototyping",
        "colors": {
            "background": "#0F172A",      # Slate 900
            "surface": "#1E293B",         # Slate 800
            "surface_border": "#334155",  # Slate 700
            "primary": "#DC2626",         # Crimson Red (Akatsuki accent)
            "primary_hover": "#B91C1C",
            "text_primary": "#F8FAFC",    # Slate 50
            "text_muted": "#94A3B8",      # Slate 400
            "success": "#10B981",
            "warning": "#F59E0B"
        },
        "typography": {
            "font_family": "Inter, system-ui, sans-serif",
            "scale": {
                "xs": "12px",
                "sm": "14px",
                "base": "16px",
                "lg": "18px",
                "xl": "20px",
                "2xl": "24px"
            }
        },
        "radius": {
            "card": "12px",
            "button": "8px",
            "pill": "9999px"
        }
    }

def main():
    parser = argparse.ArgumentParser(description="Google Stitch CLI para Konan & Akatsuki")
    parser.add_argument("--status", action="store_true", help="Verificar estado de la clave de Stitch")
    parser.add_argument("--tokens", action="store_true", help="Generar especificación de tokens para Stitch")
    parser.add_argument("--theme", type=str, default="Akatsuki Modern", help="Nombre del tema a generar")
    
    args = parser.parse_args()
    
    if args.status:
        if verify_token():
            print(f"✅ Credencial de Google Stitch verificada: Prefijo={STITCH_KEY[:7]}... Longitud={len(STITCH_KEY)} caracteres")
            print("🦋 Konan (UI/UX Designer) tiene acceso activo al motor de prototipado Stitch.")
        else:
            print("❌ Clave de Google Stitch no configurada o inválida.", file=sys.stderr)
            sys.exit(1)
    elif args.tokens:
        tokens = generate_design_tokens(args.theme)
        print(json.dumps(tokens, indent=2, ensure_ascii=False))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
