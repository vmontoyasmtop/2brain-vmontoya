#!/usr/bin/env python3
import os
import sys
import json
import csv
import subprocess
import urllib.request
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
import webbrowser

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

SPREADSHEET_ID = "1v6ev0D-3x3HTtSXWlmHDPyiG1-zB9DOTOaDd-XsJFwc"
GID = "597599129"

GSHEETS_DIR = os.path.expanduser(r"~\.gsheets-trabajo-mcp")
os.makedirs(GSHEETS_DIR, exist_ok=True)
TOKEN_PATH = os.path.join(GSHEETS_DIR, "token.json")

CREDENTIALS_PATH = os.path.expanduser(r"~\.gdocs-trabajo-mcp\credentials.json")
if not os.path.exists(CREDENTIALS_PATH):
    CREDENTIALS_PATH = os.path.expanduser(r"~\.gcal-trabajo-mcp\credentials.json")

def get_oauth_credentials():
    with open(CREDENTIALS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    web = data.get("web", {})
    return web.get("client_id"), web.get("client_secret"), web.get("redirect_uris", ["http://localhost:3000/oauth2callback"])[0]

CLIENT_ID, CLIENT_SECRET, REDIRECT_URI = get_oauth_credentials()

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly"
]

def get_access_token():
    if os.path.exists(TOKEN_PATH):
        try:
            with open(TOKEN_PATH, "r", encoding="utf-8") as f:
                tdata = json.load(f)
            req = urllib.request.Request(
                "https://oauth2.googleapis.com/token",
                data=urllib.parse.urlencode({
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET,
                    "refresh_token": tdata["refresh_token"],
                    "grant_type": "refresh_token"
                }).encode("utf-8")
            )
            with urllib.request.urlopen(req) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                return res["access_token"]
        except Exception as e:
            print(f"⚠️ Error refrescando token existente: {e}", flush=True)

    auth_code = []

    class OAuthHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            query = urllib.parse.parse_qs(parsed.query)
            if "code" in query:
                auth_code.append(query["code"][0])
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("<h1>✅ Autenticación con Google Sheets Exitosa</h1><p>Puede cerrar esta ventana y regresar a ALFRED.</p>".encode("utf-8"))
            else:
                self.send_response(400)
                self.end_headers()

        def log_message(self, format, *args):
            pass

    server = HTTPServer(("localhost", 3000), OAuthHandler)

    auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "access_type": "offline",
        "prompt": "consent"
    })

    print(f"AUTH_URL_READY: {auth_url}", flush=True)
    try:
        subprocess.run(["powershell", "-c", f'Start-Process "{auth_url}"'], check=False)
    except Exception as e:
        print(f"Start-Process error: {e}", flush=True)

    while not auth_code:
        server.handle_request()

    code = auth_code[0]
    req = urllib.request.Request(
        "https://oauth2.googleapis.com/token",
        data=urllib.parse.urlencode({
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URI
        }).encode("utf-8")
    )
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))

    save_data = {
        "type": "authorized_user",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": res.get("refresh_token")
    }
    with open(TOKEN_PATH, "w", encoding="utf-8") as f:
        json.dump(save_data, f, indent=2)

    return res["access_token"]

def main():
    token = get_access_token()
    print("✅ Token de acceso obtenido exitosamente.", flush=True)

    # 1. Descarga como CSV via export
    export_url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=csv&gid={GID}"
    req = urllib.request.Request(export_url, headers={"Authorization": f"Bearer {token}"})
    csv_path = r"C:\Users\vmontoyaMG\Desktop\2brain\raw\trabajo\reclutamiento_rrhh_mastergroup.csv"

    content = None
    try:
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode("utf-8", errors="replace")
            print(f"✅ Export CSV obtenido ({len(content)} bytes).", flush=True)
    except Exception as e:
        print(f"⚠️ Error exportando CSV: {e}. Probando Sheets API v4...", flush=True)
        api_url = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/A1:ZZ5000"
        req_api = urllib.request.Request(api_url, headers={"Authorization": f"Bearer {token}"})
        with urllib.request.urlopen(req_api) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            values = data.get("values", [])
            print(f"✅ Sheets API v4 obtuvo {len(values)} filas.", flush=True)
            import io
            out = io.StringIO()
            writer = csv.writer(out)
            for row in values:
                writer.writerow(row)
            content = out.getvalue()

    if content:
        with open(csv_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"💾 Guardado CSV en: {csv_path}", flush=True)

        lines = content.splitlines()
        print(f"\n📊 Total de líneas en CSV: {len(lines)}", flush=True)
        if lines:
            print(f"📌 Cabeceras:\n{lines[0]}\n", flush=True)
            if len(lines) > 1:
                print(f"📌 Fila 2 (Muestra):\n{lines[1]}\n", flush=True)

if __name__ == "__main__":
    main()
