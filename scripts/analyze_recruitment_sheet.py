#!/usr/bin/env python3
import json
import os
import urllib.request
import urllib.parse
import csv

SPREADSHEET_ID = "1v6ev0D-3x3HTtSXWlmHDPyiG1-zB9DOTOaDd-XsJFwc"
TOKEN_PATH = os.path.expanduser(r"~\.gsheets-trabajo-mcp\token.json")

def get_token():
    with open(TOKEN_PATH, "r", encoding="utf-8") as f:
        tdata = json.load(f)
    req = urllib.request.Request(
        "https://oauth2.googleapis.com/token",
        data=urllib.parse.urlencode({
            "client_id": tdata["client_id"],
            "client_secret": tdata["client_secret"],
            "refresh_token": tdata["refresh_token"],
            "grant_type": "refresh_token"
        }).encode("utf-8")
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))["access_token"]

def main():
    token = get_token()
    req_meta = urllib.request.Request(
        f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}",
        headers={"Authorization": f"Bearer {token}"}
    )
    with urllib.request.urlopen(req_meta) as resp:
        meta = json.loads(resp.read().decode("utf-8"))

    doc_title = meta.get("properties", {}).get("title")
    print(f"==================================================")
    print(f"DOCUMENTO: {doc_title}")
    print(f"==================================================")

    out_dir = r"C:\Users\vmontoyaMG\Desktop\2brain\raw\trabajo\recruitment_sheets"
    os.makedirs(out_dir, exist_ok=True)

    summary = []

    for s in meta.get("sheets", []):
        props = s.get("properties", {})
        sheet_id = props.get("sheetId")
        title = props.get("title")
        row_count = props.get("gridProperties", {}).get("rowCount", 0)
        col_count = props.get("gridProperties", {}).get("columnCount", 0)

        # Download CSV export for each tab
        export_url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=csv&gid={sheet_id}"
        req_export = urllib.request.Request(export_url, headers={"Authorization": f"Bearer {token}"})
        safe_title = "".join([c if c.isalnum() or c in " ._-" else "_" for c in title]).strip()
        csv_file = os.path.join(out_dir, f"{sheet_id}_{safe_title}.csv")

        try:
            with urllib.request.urlopen(req_export) as exp_resp:
                content = exp_resp.read().decode("utf-8", errors="replace")
                with open(csv_file, "w", encoding="utf-8") as f_csv:
                    f_csv.write(content)
                non_empty_lines = [l for l in content.splitlines() if l.replace(",", "").strip()]
                print(f"[*] Pestaña: '{title}' (GID: {sheet_id}) -> {len(non_empty_lines)} filas con datos.")
                summary.append({
                    "id": sheet_id,
                    "title": title,
                    "rows_with_data": len(non_empty_lines),
                    "file": csv_file
                })
        except Exception as e:
            print(f"[!] Error descargando pestaña '{title}' (GID: {sheet_id}): {e}")

    with open(os.path.join(out_dir, "summary.json"), "w", encoding="utf-8") as f_sum:
        json.dump(summary, f_sum, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
