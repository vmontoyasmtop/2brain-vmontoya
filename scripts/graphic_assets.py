"""
🎨 Graphic Assets & Brand Utility Script (Sai — Chōjū Giga Engine)
Permite generar banners publicitarios estándar, composiciones gráficas y verificar contraste WCAG.
"""

import os
import sys
import argparse
from PIL import Image, ImageDraw, ImageFont

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def hex_to_rgb(hex_str: str):
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def get_luminance(r, g, b):
    # Relación de luminancia relativa sRGB (WCAG 2.1)
    rgb = [x / 255.0 for x in (r, g, b)]
    lum = []
    for c in rgb:
        if c <= 0.03928:
            lum.append(c / 12.92)
        else:
            lum.append(((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * lum[0] + 0.7152 * lum[1] + 0.0722 * lum[2]

def check_wcag_contrast(fg_hex: str, bg_hex: str):
    fg_rgb = hex_to_rgb(fg_hex)
    bg_rgb = hex_to_rgb(bg_hex)
    l1 = get_luminance(*fg_rgb)
    l2 = get_luminance(*bg_rgb)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    ratio = (lighter + 0.05) / (darker + 0.05)
    
    aa_normal = ratio >= 4.5
    aa_large = ratio >= 3.0
    aaa_normal = ratio >= 7.0
    aaa_large = ratio >= 4.5
    
    return {
        "ratio": round(ratio, 2),
        "wcag_aa": aa_normal,
        "wcag_aa_large": aa_large,
        "wcag_aaa": aaa_normal,
        "wcag_aaa_large": aaa_large
    }

def create_gradient_banner(width: int, height: int, start_hex: str, end_hex: str, output_path: str):
    """Crea un lienzo con gradiente horizontal/diagonal suave."""
    base = Image.new('RGB', (width, height), hex_to_rgb(start_hex))
    top = Image.new('RGB', (width, height), hex_to_rgb(end_hex))
    mask = Image.new('L', (width, height))
    mask_data = []
    for y in range(height):
        for x in range(width):
            mask_data.append(int(255 * (x + y) / (width + height)))
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    base.save(output_path, quality=95)
    print(f"✅ Banner base generado con éxito: {output_path} ({width}x{height})")
    return output_path

def generate_social_post(title: str, subtitle: str, badge: str, output_path: str, format_type: str = "instagram"):
    """Genera una pieza gráfica de alta calidad para redes sociales."""
    dims = {
        "instagram": (1080, 1080),
        "story": (1080, 1920),
        "opengraph": (1200, 630),
        "banner": (1200, 400)
    }
    w, h = dims.get(format_type.lower(), (1080, 1080))
    
    # Crear fondo con gradiente elegante Slate Oscuro a Indigo
    img = Image.new('RGB', (w, h), hex_to_rgb("#0F172A"))
    draw = ImageDraw.Draw(img)
    
    # Gradiente de fondo
    start_c = hex_to_rgb("#0F172A") # slate-900
    end_c = hex_to_rgb("#1E1B4B")   # indigo-950
    for y in range(h):
        r = int(start_c[0] + (end_c[0] - start_c[0]) * (y / h))
        g = int(start_c[1] + (end_c[1] - start_c[1]) * (y / h))
        b = int(start_c[2] + (end_c[2] - start_c[2]) * (y / h))
        draw.line([(0, y), (w, y)], fill=(r, g, b))
        
    # Elementos decorativos (círculos difusos / acentos visuales)
    draw.ellipse([w - 300, -100, w + 200, 400], fill=hex_to_rgb("#312E81"), outline=None)
    draw.ellipse([-150, h - 350, 250, h + 50], fill=hex_to_rgb("#1E293B"), outline=None)
    
    # Borde de badge destacado
    badge_bg = hex_to_rgb("#10B981") # emerald-500
    badge_x = 80
    badge_y = 100
    draw.rounded_rectangle([badge_x, badge_y, badge_x + 320, badge_y + 55], radius=12, fill=badge_bg)
    draw.text((badge_x + 20, badge_y + 12), badge.upper(), fill=hex_to_rgb("#FFFFFF"))
    
    # Textos principales
    draw.text((80, badge_y + 90), title, fill=hex_to_rgb("#FFFFFF"))
    draw.text((80, badge_y + 180), subtitle, fill=hex_to_rgb("#94A3B8"))
    
    # Línea de acento inferior
    draw.rectangle([80, h - 120, w - 80, h - 116], fill=hex_to_rgb("#38BDF8"))
    draw.text((80, h - 90), "Desarrollado con grado militar por la Organización Akatsuki", fill=hex_to_rgb("#64748B"))
    
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path, quality=95)
    print(f"✅ Pieza publicitaria generada: {output_path} [{format_type.upper()} - {w}x{h}]")
    return output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sai Chōjū Giga - Generador de Assets Gráficos")
    parser.add_argument("--check-contrast", nargs=2, metavar=("FG", "BG"), help="Verificar contraste WCAG entre dos colores HEX")
    parser.add_argument("--post", action="store_true", help="Generar pieza para redes sociales")
    parser.add_argument("--title", default="EL CUADRE POS", help="Título principal")
    parser.add_argument("--subtitle", default="Cierre de caja en 3 min sin internet", help="Subtítulo o hook")
    parser.add_argument("--badge", default="100% OFFLINE EDGE", help="Texto del badge")
    parser.add_argument("--format", default="instagram", choices=["instagram", "story", "opengraph", "banner"])
    parser.add_argument("--output", default="wiki/proyectos/assets/banner_sai.png", help="Ruta de salida")
    
    args = parser.parse_args()
    
    if args.check_contrast:
        res = check_wcag_contrast(args.check_contrast[0], args.check_contrast[1])
        print(f"🎨 Contraste {args.check_contrast[0]} sobre {args.check_contrast[1]}: Ratio {res['ratio']}:1")
        print(f"   WCAG AA (Normal): {'PASS ✅' if res['wcag_aa'] else 'FAIL ❌'}")
        print(f"   WCAG AAA (Normal): {'PASS ✅' if res['wcag_aaa'] else 'FAIL ❌'}")
    elif args.post:
        generate_social_post(args.title, args.subtitle, args.badge, args.output, args.format)
    else:
        parser.print_help()
