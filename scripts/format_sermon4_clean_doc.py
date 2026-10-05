#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Oficial ALFRED / Docs Expert:
Formateo y Reducción del Documento Oficial de Google Docs del Sermón 4
Aplica Protocolo Docs Expert: Sin Markdown crudo, sin separadores ASCII, 
longitud reducida (~3.5 a 4 páginas) y estilos limpios para púlpito personal.
Doc ID: 1_hZA4qFSE7S8l3zNf2zaIPLMUE6EeSe_xGbDobSu2Ys
"""

import os
import sys
import json
import urllib.request
import urllib.parse

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GDOCS_DIR = os.path.expanduser(r"~\.gdocs-trabajo-mcp")
TOKEN_PATH = os.path.join(GDOCS_DIR, "token.json")
CREDENTIALS_PATH = os.path.join(GDOCS_DIR, "credentials.json")
TARGET_DOC_ID = "1_hZA4qFSE7S8l3zNf2zaIPLMUE6EeSe_xGbDobSu2Ys"

def get_access_token():
    with open(CREDENTIALS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    web = data.get("web", {})
    client_id = web.get("client_id")
    client_secret = web.get("client_secret")

    with open(TOKEN_PATH, "r", encoding="utf-8") as f:
        tdata = json.load(f)

    req = urllib.request.Request(
        "https://oauth2.googleapis.com/token",
        data=urllib.parse.urlencode({
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": tdata["refresh_token"],
            "grant_type": "refresh_token"
        }).encode("utf-8")
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        return res["access_token"]

def build_clean_sermon_doc(token):
    # Texto limpio estructurado sin Markdown plano ni caracteres toscos
    sections = [
        ("TITLE", "SERMÓN 4: DE APRENDIZ A MULTIPLICADOR (EL CICLO DE LA VIDA)"),
        ("SUBTITLE", "Serie: Caminando Juntos — De Creyentes a Discípulos | Área Ministerial"),
        ("NORMAL", "Pastor Víctor Montoya | Guía de Púlpito & Estudio Bíblico"),
        ("NORMAL", "Pasajes Clave: Hebreos 5:11-14 | 2 Timoteo 2:1-2 | 1 Corintios 11:1 | Tiempo Estimado: 35 a 40 minutos\n"),
        
        ("HEADING_1", "PROPOSICIÓN CENTRAL (BIG IDEA)"),
        ("QUOTE", "«La verdadera madurez espiritual jamás se mide por cuánta Biblia cabe en tu cabeza, sino por cuántas vidas estás alimentando con el amor de Cristo: el discipulado bíblico no concluye cuando aprendes a seguir a Jesús, sino cuando enseñas a otros a seguirle.»\n"),
        
        ("HEADING_1", "I. APERTURA: EL ENIGMA DE LOS DOS MARES"),
        ("NORMAL", "• Recapitulación de la Serie:\n  1. Salir de la multitud para sentarnos a la Mesa con Cristo (Sermón 1).\n  2. Abrazar el modelo de comunidad sin llaneros solitarios (Sermón 2).\n  3. Desmantelar el orgullo y cultivar un corazón enseñable (Sermón 3).\n  4. Recibir la estafeta de la fe y multiplicarnos en otros (Sermón 4)."),
        ("NORMAL", "• La Paradoja de los Dos Mares de Israel:\n  - En la Tierra Santa fluye un único río vital: el río Jordán. Este río alimenta dos grandes masas de agua con destinos completamente opuestos:\n  1. El Mar de Galilea: Recibe el agua dulce del Jordán por el norte y de inmediato la deja fluir hacia el sur para regar los valles. Es un lago cristalino, desbordante de peces, riberas verdes y aldeas prósperas. Vive porque da lo que recibe.\n  2. El Mar Muerto: Recibe exactamente la misma agua dulce del río Jordán, pero tiene una sola regla: todo lo recibe y nada entrega. No tiene afluente de salida. El sol implacable evapora el agua y deja una concentración tóxica de sal y azufre donde ningún pez puede nadar y ninguna planta puede echar raíces."),
        ("NORMAL", "• Pregunta de Diagnóstico al Corazón:\n  ¿Eres un creyente Mar de Galilea o un creyente Mar Muerto? La fe que solo consume sermones y jamás cuida a nadie termina amarga, salobre e infértil.\n"),
        
        ("HEADING_1", "II. PUNTO 1: LA TRAMPA DE LA INMADUREZ CRÓNICA (DE CONSUMIDORES A CUIDADORES)"),
        ("NORMAL", "Texto Bíblico — Hebreos 5:11-14 (RVR1960):"),
        ("SCRIPTURE", "«Porque debiendo ser ya maestros, después de tanto tiempo, tenéis necesidad de que se os vuelva a enseñar cuáles son los primeros rudimentos de las palabras de Dios; y habéis llegado a ser tales que tenéis necesidad de leche, y no de alimento sólido. Y todo aquel que participa de la leche es inexperto en la palabra de justicia, porque es niño; pero el alimento sólido es para los que han alcanzado madurez, para los que por el uso tienen los sentidos ejercitados en el discernimiento del bien y del mal.»"),
        ("NORMAL", "• La Deuda Moral (Opheilontes):\n  El autor de Hebreos denuncia que el paso de los años sin reproducción espiritual es una deuda moral con Dios. Llevar 10 o 20 años en una congregación consumiendo doctrina sin ser capaz de alimentar a un nuevo hermano es una anomalía."),
        ("NORMAL", "• La Parábola del Adulto en Pañales:\n  Un bebé de 4 meses en pañales y tomando tetero es tierno; un hombre de 35 años con barba y canas que use pañales y llore por compota en la boca es una tragedia médica. En las iglesias hay creyentes veteranos que siguen usando pañales espirituales: se ofenden por cualquier detalle y no saben orar por sí mismos."),
        ("NORMAL", "• El Salto de Madurez:\n  Una persona madura biológicamente el día en que deja de exigir que sus padres lo alimenten y comienza a alimentar a sus propios hijos. En el Reino de Dios es idéntico: tu fe madura de golpe el día en que asumes la responsabilidad de mentorear y cuidar a otro."),
        ("NORMAL", "• El Gimnasio de la Gracia (Gegymnasmena):\n  El discernimiento no cae del cielo por ósmosis. Se forja en el gimnasio del servicio práctico al sentarte a orar, aconsejar con la Biblia y cuidar tu testimonio delante de un hermano más joven.\n"),
        
        ("HEADING_1", "III. PUNTO 2: LA ECUACIÓN SAGRADA DE LA MULTIPLICACIÓN (LAS 4 GENERACIONES)"),
        ("NORMAL", "Texto Bíblico — 2 Timoteo 2:1-2 (RVR1960):"),
        ("SCRIPTURE", "«Tú, pues, hijo mío, esfuérzate en la gracia que es en Cristo Jesús. Lo que has oído de mí ante muchos testigos, esto encarga a hombres fieles que sean idóneos para enseñar también a otros.»"),
        ("NORMAL", "• Contexto Histórico:\n  Pablo escribe desde la prisión mamertina en Roma, encadenado, a las puertas de su ejecución bajo Nerón. En su despedida, no pide edificios ni proyectos humanos; deja la estrategia suprema de multiplicación generacional."),
        ("NORMAL", "• La Cadena de 4 Generaciones:\n  1ª Generación: Pablo (El Mentor).\n  2ª Generación: Timoteo (El Aprendiz).\n  3ª Generación: Hombres Fieles (Los Multiplicadores Locales).\n  4ª Generación: Otros También (La Expansión Fecunda del Reino)."),
        ("NORMAL", "• El Sagrado Fideicomiso (Parathou):\n  En el derecho mercantil romano, parathēkē era un depósito en custodia inviolable. El evangelio no es una propiedad privada para nuestro disfrute; es un fideicomiso sagrado para entregar intacto a la siguiente generación."),
        ("NORMAL", "• Adición vs. Multiplicación Geométrica:\n  - Un evangelista ganando 1,000 personas diarias durante 30 años = 11 millones de almas.\n  - Un creyente común discipulando a 1 sola persona al año por multiplicación (1, 2, 4, 8, 16, 32...) = en 33 años se alcanza a más de 8,500 millones de personas (toda la población de la Tierra). Jesús no invirtió su vida en las masas volubles, sino en Doce hombres para transformar el mundo."),
        ("NORMAL", "• El Filtro Bíblico F.A.T. del Discípulo:\n  - F — Fieles (Pistois): De fiar, constantes, cumplen sus compromisos.\n  - A — Accesibles / Disponibles: Con espacio real en la agenda para Dios.\n  - T — Enseñables (Teachable): Humildes para dejarse orientar sin ofenderse."),
        ("NORMAL", "• La Ilustración de la Estafeta Olímpica 4x100m:\n  La carrera de relevos se gana o se pierde en la zona de transferencia de la estafeta. Si el testigo cae al suelo, todo el equipo queda descalificado. Que la estafeta de la fe jamás caiga al suelo en nuestra generación.\n"),
        
        ("HEADING_1", "IV. PUNTO 3: TU VIDA ES EL PLAN DE ESTUDIOS"),
        ("NORMAL", "Texto Bíblico — 1 Corintios 11:1 (RVR1960):"),
        ("SCRIPTURE", "«Sed imitadores de mí, así como yo de Cristo.»"),
        ("NORMAL", "• Vencer el Síndrome del Impostor:\n  El diablo te susurra: 'Tú no sabes suficiente, tienes demasiados defectos'. Pero Pablo no dijo 'mírenme porque soy perfecto'; dijo 'imítenme en la medida en que yo sigo a Cristo'. No se exige perfección fingida, sino una dirección clara hacia la cruz."),
        ("NORMAL", "• La Verdad se Atrapa en el Camino:\n  El discipulado no es dictar una clase teórica; es abrir la mesa del hogar con un café y modelar la fe real: cómo tratas a tu cónyuge cuando estás cansado, cómo oras cuando las finanzas aprietan y cómo pides perdón cuando te equivocas."),
        ("NORMAL", "• La Invitación del Multiplicador:\n  'Hermano, yo no tengo todas las respuestas; pero conozco al Pastor que guía mis pasos. Toma mi mano y caminemos juntos detrás de Jesús.'\n"),
        
        ("HEADING_1", "V. CONCLUSIÓN & LLAMADO AL ALTAR: LANZAMIENTO 'CAMINANDO JUNTOS'"),
        ("NORMAL", "• Recapitulación de los 4 Peldaños de la Serie:\n  1. Salir de la multitud para sentarse a la Mesa con Cristo.\n  2. Abrazar la comunidad sin llaneros solitarios.\n  3. Humillar el corazón ante la corrección santa.\n  4. Recibir la estafeta y multiplicarse en otros."),
        ("NORMAL", "• El Doble Llamado al Altar:\n  - Llamado 1: Para quienes reconocen con humildad que necesitan un mentor espiritual que camine a su lado.\n  - Llamado 2: Para quienes Dios llama hoy a levantarse como multiplicadores, abrir su casa y discipular a otros."),
        ("NORMAL", "• Oración de Ministración Pastoral:\n  Rompimiento de la esterilidad y de la pasividad espiritual; unción y bendición sobre las nuevas parejas de discipulado del programa 'Caminando Juntos'.\n"),
        
        ("HEADING_1", "VI. SÍNTESIS EXEGÉTICA DE TÉRMINOS CLAVE (GRIEGO KOINÉ)"),
        ("NORMAL", "• Parathou (παράθου - 2 Timoteo 2:2): Imperativo aoristo de paratithēmi. Término técnico mercantil para un depósito en custodia o fideicomiso inviolable.\n• Pistois Anthrōpois (πιστοῖς ἀνθρώποις - 2 Timoteo 2:2): Hombres fieles, leales y probados que garantizan la pureza del relevo generacional.\n• Hikanoi (ἱκανοί - 2 Timoteo 2:2): Competentes, aptos y capacitados para enseñar a otros.\n• Opheilontes (ὀφείλοντες - Hebreos 5:12): Deuda moral obligatoria contraída por el tiempo transcurrido en la fe sin reproducción espiritual.\n• Gegymnasmena (γεγυμνασμένα - Hebreos 5:14): Sentidos espirituales entrenados en el gimnasio del discipulado práctico y la vida compartida.\n• Mimētai (μιμηταί - 1 Corintios 11:1): Modeladores vivos de la verdad encarnada en la conducta cotidiana.\n"),
        
        ("HEADING_1", "VII. GUÍA DE PREGUNTAS PARA CÉLULAS Y GRUPOS DE HOGAR"),
        ("NORMAL", "1. Al comparar tu vida con el Mar de Galilea y el Mar Muerto, ¿en cuál estado te has encontrado recientemente?\n2. ¿Cuánto tiempo llevas en la fe y qué pasos concretos darás para pasar de consumidor a cuidador de otros?\n3. ¿Quién fue el mentor que más impactó tu vida y qué aprendiste de su ejemplo?\n4. Del perfil F.A.T. (Fiel, Accesible, Enseñable), ¿cuál es tu mayor fortaleza y cuál debes cultivar más?\n5. ¿A qué persona específica invitarás esta semana para orar y comenzar a caminar juntos?")
    ]

    # 1. Obtener longitud actual del documento para limpiarlo
    req_get = urllib.request.Request(
        f"https://docs.googleapis.com/v1/documents/{TARGET_DOC_ID}",
        headers={"Authorization": f"Bearer {token}"}
    )
    with urllib.request.urlopen(req_get, timeout=15) as r:
        doc = json.loads(r.read().decode("utf-8"))
    end_index = doc.get("body", {}).get("content", [])[-1].get("endIndex", 1) - 1

    # 2. Limpiar todo el contenido viejo
    if end_index > 1:
        req_del = urllib.request.Request(
            f"https://docs.googleapis.com/v1/documents/{TARGET_DOC_ID}:batchUpdate",
            data=json.dumps({"requests": [{
                "deleteContentRange": {
                    "range": {"startIndex": 1, "endIndex": end_index}
                }
            }]}).encode("utf-8"),
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        )
        urllib.request.urlopen(req_del, timeout=15)
        print("🧹 Contenido anterior de 20 páginas eliminado.")

    # 3. Construir el texto completo y registrar los rangos para aplicar estilos nativos de Google Docs
    full_text = ""
    ranges = [] # list of (type, start, end)

    current_idx = 1
    for sec_type, sec_text in sections:
        start = current_idx
        text_with_nl = sec_text + "\n"
        full_text += text_with_nl
        current_idx += len(text_with_nl)
        end = current_idx - 1
        ranges.append((sec_type, start, end))

    # Insertar el texto conciso limpio
    req_ins = urllib.request.Request(
        f"https://docs.googleapis.com/v1/documents/{TARGET_DOC_ID}:batchUpdate",
        data=json.dumps({"requests": [{
            "insertText": {
                "location": {"index": 1},
                "text": full_text
            }
        }]}).encode("utf-8"),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    )
    urllib.request.urlopen(req_ins, timeout=15)
    print("📝 Texto conciso insertado con éxito.")

    # 4. Aplicar estilos nativos enriquecidos (Headings, negritas, cursivas bíblicas)
    style_requests = []
    
    # Fuente estándar legible para todo el documento
    style_requests.append({
        "updateTextStyle": {
            "range": {"startIndex": 1, "endIndex": current_idx - 1},
            "textStyle": {
                "weightedFontFamily": {"fontFamily": "Georgia"},
                "fontSize": {"magnitude": 10.5, "unit": "PT"},
                "foregroundColor": {"color": {"rgbColor": {"red": 0.15, "green": 0.15, "blue": 0.15}}}
            },
            "fields": "weightedFontFamily,fontSize,foregroundColor"
        }
    })

    for sec_type, start, end in ranges:
        if sec_type == "TITLE":
            style_requests.append({
                "updateParagraphStyle": {
                    "range": {"startIndex": start, "endIndex": end},
                    "paragraphStyle": {"namedStyleType": "TITLE"},
                    "fields": "namedStyleType"
                }
            })
            style_requests.append({
                "updateTextStyle": {
                    "range": {"startIndex": start, "endIndex": end},
                    "textStyle": {
                        "bold": True,
                        "fontSize": {"magnitude": 18, "unit": "PT"},
                        "foregroundColor": {"color": {"rgbColor": {"red": 0.1, "green": 0.2, "blue": 0.4}}}
                    },
                    "fields": "bold,fontSize,foregroundColor"
                }
            })
        elif sec_type == "SUBTITLE":
            style_requests.append({
                "updateTextStyle": {
                    "range": {"startIndex": start, "endIndex": end},
                    "textStyle": {
                        "italic": True,
                        "fontSize": {"magnitude": 11, "unit": "PT"},
                        "foregroundColor": {"color": {"rgbColor": {"red": 0.4, "green": 0.4, "blue": 0.4}}}
                    },
                    "fields": "italic,fontSize,foregroundColor"
                }
            })
        elif sec_type == "HEADING_1":
            style_requests.append({
                "updateParagraphStyle": {
                    "range": {"startIndex": start, "endIndex": end},
                    "paragraphStyle": {"namedStyleType": "HEADING_1"},
                    "fields": "namedStyleType"
                }
            })
            style_requests.append({
                "updateTextStyle": {
                    "range": {"startIndex": start, "endIndex": end},
                    "textStyle": {
                        "bold": True,
                        "fontSize": {"magnitude": 13, "unit": "PT"},
                        "foregroundColor": {"color": {"rgbColor": {"red": 0.12, "green": 0.25, "blue": 0.45}}}
                    },
                    "fields": "bold,fontSize,foregroundColor"
                }
            })
        elif sec_type in ("QUOTE", "SCRIPTURE"):
            style_requests.append({
                "updateTextStyle": {
                    "range": {"startIndex": start, "endIndex": end},
                    "textStyle": {
                        "italic": True,
                        "fontSize": {"magnitude": 10.5, "unit": "PT"},
                        "foregroundColor": {"color": {"rgbColor": {"red": 0.1, "green": 0.35, "blue": 0.25}}}
                    },
                    "fields": "italic,fontSize,foregroundColor"
                }
            })

    req_styles = urllib.request.Request(
        f"https://docs.googleapis.com/v1/documents/{TARGET_DOC_ID}:batchUpdate",
        data=json.dumps({"requests": style_requests}).encode("utf-8"),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    )
    urllib.request.urlopen(req_styles, timeout=15)
    print("🎨 Estilos nativos de Google Docs (Títulos, Citas Bíblicas y Tipografía Georgia) aplicados exitosamente.")

    print(f"👉 URL Oficial de Google Docs: https://docs.google.com/document/d/{TARGET_DOC_ID}/edit")

if __name__ == "__main__":
    t = get_access_token()
    build_clean_sermon_doc(t)
