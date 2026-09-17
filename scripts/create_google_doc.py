#!/usr/bin/env python3
import os
import sys
import json
import urllib.request
import urllib.parse
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GDOCS_DIR = os.path.expanduser(r"~\.gdocs-trabajo-mcp")
TOKEN_PATH = os.path.join(GDOCS_DIR, "token.json")
CREDENTIALS_PATH = os.path.join(GDOCS_DIR, "credentials.json")
if not os.path.exists(CREDENTIALS_PATH):
    CREDENTIALS_PATH = os.path.expanduser(r"~\.gcal-trabajo-mcp\credentials.json")

def get_oauth_credentials():
    with open(CREDENTIALS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    web = data.get("web", {})
    return web.get("client_id"), web.get("client_secret"), web.get("redirect_uris", ["http://localhost:3000/oauth2callback"])[0]

CLIENT_ID, CLIENT_SECRET, REDIRECT_URI = get_oauth_credentials()
SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive.file"
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
            print(f"⚠️ Error al refrescar token existente: {e}")

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
                self.wfile.write("<h1>✅ Autenticación con Google Docs Exitosa</h1><p>Puede cerrar esta ventana y regresar a ALFRED.</p>".encode("utf-8"))
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
    
    print(f"🔑 Abriendo navegador para autorizar Google Docs en soporte@mastergroupve.com...")
    webbrowser.open(auth_url)
    
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

if __name__ == "__main__":
    token = get_access_token()
    print(f"Token listo para operar.")
