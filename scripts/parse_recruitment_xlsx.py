#!/usr/bin/env python3
import zipfile
import xml.etree.ElementTree as ET
import os
import sys
import json
import csv

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

XLSX_PATH = r"C:\Users\vmontoyaMG\Desktop\2brain\raw\trabajo\Control_de_Reclutamiento.xlsx"
OUTPUT_DIR = r"C:\Users\vmontoyaMG\Desktop\2brain\raw\trabajo\recruitment_parsed"
os.makedirs(OUTPUT_DIR, exist_ok=True)

NS = {
    'main': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
    'rel': 'http://schemas.openxmlformats.org/package/2006/relationships'
}

def parse_shared_strings(z):
    if 'xl/sharedStrings.xml' not in z.namelist():
        return []
    tree = ET.fromstring(z.read('xl/sharedStrings.xml'))
    strings = []
    for si in tree.findall('main:si', NS):
        # Could be simple <t> or complex formatted <r><t>
        texts = []
        for t in si.findall('.//main:t', NS):
            if t.text:
                texts.append(t.text)
        strings.append("".join(texts))
    return strings

def parse_sheet(z, sheet_rel_path, shared_strings):
    tree = ET.fromstring(z.read(sheet_rel_path))
    rows_data = []
    
    # helper to convert col letters to 0-based index
    def col_to_idx(col_str):
        idx = 0
        for char in col_str:
            idx = idx * 26 + (ord(char) - ord('A') + 1)
        return idx - 1

    for row_elem in tree.findall('.//main:row', NS):
        r_num = int(row_elem.attrib.get('r', 0))
        cells_dict = {}
        for c in row_elem.findall('main:c', NS):
            cell_ref = c.attrib.get('r', '')
            # Separate col letters and row number
            col_letters = "".join([ch for ch in cell_ref if ch.isalpha()])
            col_idx = col_to_idx(col_letters) if col_letters else 0
            
            cell_type = c.attrib.get('t', 'n')
            val_elem = c.find('main:v', NS)
            val = val_elem.text if val_elem is not None else ""
            
            if cell_type == 's' and val.isdigit():
                val = shared_strings[int(val)] if int(val) < len(shared_strings) else val
            elif cell_type == 'b':
                val = "TRUE" if val == "1" else "FALSE"
            elif cell_type == 'inlineStr':
                is_elem = c.find('.//main:t', NS)
                val = is_elem.text if is_elem is not None else ""
            
            cells_dict[col_idx] = val
            
        if cells_dict:
            max_col = max(cells_dict.keys())
            row_list = [cells_dict.get(i, "") for i in range(max_col + 1)]
            # check if row is not all empty
            if any(str(x).strip() for x in row_list):
                rows_data.append((r_num, row_list))
                
    return rows_data

def main():
    with zipfile.ZipFile(XLSX_PATH, 'r') as z:
        shared_strings = parse_shared_strings(z)
        
        wb_tree = ET.fromstring(z.read('xl/workbook.xml'))
        sheets_elem = wb_tree.find('main:sheets', NS)
        
        # Read workbook rels to map r:id to target file
        rels_tree = ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
        rel_map = {}
        for r in rels_tree:
            rel_map[r.attrib['Id']] = r.attrib['Target']

        report = {}
        
        for s in sheets_elem:
            name = s.attrib.get('name')
            r_id = s.attrib.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
            target = rel_map.get(r_id)
            if not target.startswith('xl/'):
                target = 'xl/' + target
                
            rows = parse_sheet(z, target, shared_strings)
            safe_name = "".join([c if c.isalnum() or c in " ._-" else "_" for c in name]).strip()
            csv_path = os.path.join(OUTPUT_DIR, f"{safe_name}.csv")
            
            with open(csv_path, 'w', encoding='utf-8', newline='') as f_csv:
                writer = csv.writer(f_csv)
                for r_num, row_vals in rows:
                    writer.writerow(row_vals)
                    
            print(f"==================================================")
            print(f"📄 PESTAÑA: '{name}' | Total filas con datos: {len(rows)}")
            print(f"💾 Guardado CSV en: {csv_path}")
            if rows:
                print(f"  📌 Fila 1 ({len(rows[0][1])} cols): {rows[0][1][:8]}")
                if len(rows) > 1:
                    print(f"  📌 Fila 2 ({len(rows[1][1])} cols): {rows[1][1][:8]}")
                if len(rows) > 2:
                    print(f"  📌 Fila 3 ({len(rows[2][1])} cols): {rows[2][1][:8]}")
                    
            report[name] = {
                "total_rows": len(rows),
                "csv_path": csv_path,
                "sample_rows": [r[1][:10] for r in rows[:4]]
            }
            
        with open(os.path.join(OUTPUT_DIR, "audit_summary.json"), 'w', encoding='utf-8') as f_rep:
            json.dump(report, f_rep, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    main()
