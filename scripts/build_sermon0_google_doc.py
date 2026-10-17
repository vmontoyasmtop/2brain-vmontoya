#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Oficial ALFRED / Docs Expert:
Creación del Documento Oficial de Google Docs del Sermón 0 (Estudio, Ejemplos de Vida & Panorama).
Formato limpio y optimizado para impresión (Púlpito / Estudio Pastoral).
Cuenta Personal: vmontoya.smartopsve@gmail.com
"""

import os
import sys
import json
import time
import urllib.request
import urllib.parse

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GDOCS_DIR = os.path.expanduser(r"~\.gdocs-trabajo-mcp")
TOKEN_PATH = os.path.join(GDOCS_DIR, "token.json")
CREDENTIALS_PATH = os.path.join(GDOCS_DIR, "credentials.json")
PERSONAL_EMAIL = "vmontoya.smartopsve@gmail.com"

def safe_urlopen(req, retries=5, delay=2):
    for attempt in range(retries):
        try:
            return urllib.request.urlopen(req, timeout=30)
        except Exception as e:
            if attempt == retries - 1:
                raise e
            time.sleep(delay * (attempt + 1))

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
    resp = safe_urlopen(req)
    res = json.loads(resp.read().decode("utf-8"))
    return res["access_token"]

def create_google_doc(access_token):
    title = "⛪ SERMÓN 0: Jesús y la Vida Real (Guía de Estudio & Ejemplos de Vida)"
    
    # 1. Crear documento en Google Docs
    req_create = urllib.request.Request(
        "https://docs.googleapis.com/v1/documents",
        data=json.dumps({"title": title}).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    )
    resp_create = safe_urlopen(req_create)
    doc_data = json.loads(resp_create.read().decode("utf-8"))
    doc_id = doc_data["documentId"]
    print(f"📄 Documento creado en Google Docs. ID: {doc_id}")

    # 2. Contenido preparado y limpio para imprimir
    printable_text = """================================================================================
SERMÓN 0: JESÚS Y LA VIDA REAL (EL MANIFIESTO DEL REINO)
Serie de Sermones: Jesús, Solución a Todo Problema (Filipenses 4:13)
Guía de Estudio Teológico, Exégesis & Ejemplos de Vida para Púlpito
================================================================================

PASAJES BÍBLICOS CLAVE:
• Juan 16:33 — «En el mundo tendréis aflicción; pero confiad, yo he vencido al mundo.»
• Juan 17:14-19 — «No ruego que los quites del mundo, sino que los guardes del mal.»
• Mateo 5:13-16 — «Vosotros sois la sal de la tierra... Vosotros sois la luz del mundo.»
• Filipenses 4:11-13 — «Todo lo puedo en Cristo que me fortalece.»

PROPOSICIÓN CENTRAL (GRAN TESIS):
"Jesús no vino únicamente a darnos un boleto de entrada al cielo, sino a modelar e impartirnos el poder para vivir como vencedores en la tierra frente a cada problema humano."

================================================================================
I. MARCO TEOLÓGICO: LOS DOS EXTREMOS vs. EL DISEÑO DE JESÚS
================================================================================

1. EL EXTREMO DEL ESCAPISMO MÍGICO:
   - Cree que la fe es una burbuja que elimina automáticamente el dolor, las crisis y las pruebas.
   - Colapsa ante la primera dificultad porque asume que el problema es falta de fe.

2. EL EXTREMO DEL CONFORMISMO DERROTADO:
   - Limita a Dios al templo el domingo, pero de lunes a sábado vive aplastado por el mismo estrés, miedo y amargura que el mundo secular.

3. EL DISEÑO DE JESÚS (JUAN 17:15-18):
   - «En el mundo, pero no del mundo»: No nos saca del planeta, sino que nos preserva del mal y nos capacita para manifestar el gobierno de Dios en medio de la realidad cotidiana.

================================================================================
II. RAÍCES EXEGÉTICAS EN GRIEGO (HERRAMIENTAS PARA EL ESTUDIO)
================================================================================

1. THLIPSIS (θλῖψις — Juan 16:33a):
   - Significado: Presión aplastante, como la piedra del lagar que prensa las uvas.
   - Enseñanza: La aflicción es ineludible en un mundo caído. No es ausencia de Dios; es el terreno donde la fe se manifiesta.

2. THARSEITE (θαρσεῖτε — Juan 16:33b):
   - Significado: Imperativo presente continuo: «¡Tened valor y aliento de forma constante!».

3. NENIKĒKA (νενίκηκα — Juan 16:33c):
   - Significado: Pretérito perfecto de nikaō: Victoria consumada y permanente.
   - Enseñanza: No luchamos para ganar, sino que batallamos desde la victoria consumada de Cristo.

4. TĒREŌ EK TOU PONĒROU (τηρέω ἐκ τοῦ πονηροῦ — Juan 17:15):
   - Significado: Montar guardia activa / custodiar un tesoro del mal en medio del mundo.

5. ENDYNAMOUNTI (ἐνδυναμοῦντι — Filipenses 4:13):
   - Significado: Participio presente: «En Aquel que continuamente me infunde poder interior».
   - Enseñanza: Cristo no nos tira una cuerda desde lejos; entra en nuestro interior para sostenernos.

================================================================================
III. LOS 4 ESCENARIOS DE LA VIDA REAL: DIAGNÓSTICO, MODELO & EJEMPLOS BÍBLICOS
================================================================================

--------------------------------------------------------------------------------
ESCENARIO 1: FRENTE A LA INSATISFACCIÓN, LA ANSIEDAD Y EL AFÁN (SERMÓN 1)
--------------------------------------------------------------------------------
• El Problema: Cultura de hiperconsumo, comparación en redes, mentes divididas (merimna) y estrés financiero crónico.
• La Solución en Jesús: El secreto del contentamiento radical (autarkēs) y el descanso en el cuidado providencial del Padre (Mateo 6:25-34).
• Ejemplos Bíblicos de Vida:
  [X] Marta de Betania (Lucas 10:38-42): Teniendo a Jesús en su casa, estaba afanada y turbada, quejándose y juzgando a su hermana.
  [X] Rey Acab (1 Reyes 21:1-4): En un palacio de marfil, cayó en depresión infantil porque no pudo comprar la viña de Nabot (insatisfacción crónica).
  [V] Apóstol Pablo (Filipenses 4:10-13): En un calabozo romano frío, pleno y en victoria: «He aprendido a contentarme... Todo lo puedo en Cristo».
  [V] La Viuda de Sarepta (1 Reyes 17:8-16): Con solo un puñado de harina confió en la palabra de Dios y la tinaja nunca escaseó.

--------------------------------------------------------------------------------
ESCENARIO 2: FRENTE AL MIEDO Y LAS CRISIS IMPREVISTAS (SERMÓN 2)
--------------------------------------------------------------------------------
• El Problema: Pánico, parálisis emocional y angustia ante diagnósticos, pérdidas o tormentas inesperadas.
• La Solución en Jesús: La paz sobrenatural (eirēnē) que no depende de la calma exterior, sino del gobierno de Cristo en la barca (Marcos 4:35-41 / Juan 14:27).
• Ejemplos Bíblicos de Vida:
  [X] Los Discípulos en el Mar de Galilea (Marcos 4:35-41): Pescadores experimentados en pánico gritando «¿no tienes cuidado que perecemos?», mirando el tamaño de las olas en vez de mirar al Dueño del mar que dormía a bordo.
  [V] Sadrac, Mesac y Abed-nego (Daniel 3:16-18): Ante el horno de fuego ardiendo siete veces más: «Nuestro Dios puede librarnos; y si no, no nos postraremos ante tus dioses».
  [V] Daniel en el Foso de los Leones (Daniel 6:10-23): Orando con reposo y ventanas abiertas mientras Dios cerraba la boca de las fieras.

--------------------------------------------------------------------------------
ESCENARIO 3: FRENTE AL CONFLICTO Y LAS RELACIONES QUEBRADAS (SERMÓN 3)
--------------------------------------------------------------------------------
• El Problema: Rencor acumulado, venganza («ojo por ojo»), aislamiento defensivo y heridas matrimoniales/familiares.
• La Solución en Jesús: La gracia y el perdón radical (aphiēmi), absorbiendo la ofensa y restaurando relaciones caídas (Mateo 5:38-48 / Efesios 4:31-32).
• Ejemplos Bíblicos de Vida:
  [X] Absalón (2 Samuel 13:20-29): Dos años de odio silencioso que terminaron en homicidio, conspiración y ruina familiar.
  [X] El Siervo Despiadado (Mateo 18:23-35): Perdonado de 10.000 talentos, fue y ahogó a su consiervo por 100 denarios.
  [V] José en Egipto (Génesis 45 y 50): Traicionado y encarcelado 13 años por sus hermanos; al tenerlos a sus pies los abrazó y perdonó: «Vosotros pensasteis mal contra mí, mas Dios lo encaminó a bien para salvar vidas».
  [V] Esteban (Hechos 7:59-60): Apedreado hasta la muerte orando por sus verdugos: «Señor, no les tomes en cuenta este pecado».

--------------------------------------------------------------------------------
ESCENARIO 4: FRENTE AL VACÍO EXISTENCIAL Y LA RUTINA (SERMÓN 4)
--------------------------------------------------------------------------------
• El Problema: Monotonía, crisis de identidad y el sinsentido de existir únicamente para pagar cuentas y morir.
• La Solución en Jesús: La grandeza en el servicio (diakonia) y la misión eterna de ser sal de la tierra y luz del mundo (Mateo 20:25-28 / Mateo 5:13-16 / Juan 17:18).
• Ejemplos Bíblicos de Vida:
  [X] Rey Salomón (Eclesiastés 2:1-11): Lo tuvo todo (dinero, fama, placeres, arquitectura) y concluyó: «Todo era vanidad, vacío y aflicción de espíritu debajo del sol».
  [V] Simón Pedro (Lucas 5:1-11): Tras una noche de pesca estéril con redes vacías, Jesús sube a su barca y lo transforma en pescador de almas.
  [V] Nehemías (Nehemías 1-2): Dejó el confort del palacio persa para liderar la reconstrucción de los muros y la dignidad de su pueblo.

================================================================================
IV. CÓMO ENLAZAR Y ESTABLECER EL SERMÓN 0 EN EL PÚLPITO
================================================================================

1. EL ANCLA INICIAL (Minutos 0 - 10):
   - Presentar la tensión entre el Escapismo y el Conformismo.
   - Lectura solemne de Juan 16:33 y Juan 17:15.

2. EL MAPA DE LOS 4 ENFOQUES (Minutos 10 - 25):
   - Exponer los 4 cuadrantes con sus contrastes bíblicos (Marta vs. Pablo, Discípulos vs. Daniel, Absalón vs. José, Salomón vs. Pedro).

3. LA LLAVE MAESTRA (Minutos 25 - 35):
   - Explicar Filipenses 4:13: La fuerza no es esfuerzo humano; es la vida de Cristo (endynamounti) operando en el creyente.

4. MINISTRACIÓN & LLAMADO AL ALTAR (Minutos 35 - 40):
   - Invitar a la congregación a consagrarse para el proceso de transformación que Dios traerá en toda la serie.
"""

    # 3. Insertar texto en el documento
    requests = [{
        "insertText": {
            "location": {"index": 1},
            "text": printable_text
        }
    }]

    req_update = urllib.request.Request(
        f"https://docs.googleapis.com/v1/documents/{doc_id}:batchUpdate",
        data=json.dumps({"requests": requests}).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    )
    safe_urlopen(req_update)
    print("✅ Contenido insertado con éxito en el documento.")

    # 4. Otorgar permisos a la cuenta personal (vmontoya.smartopsve@gmail.com) como editor y a cualquiera con el link como lector
    try:
        perm_personal = urllib.request.Request(
            f"https://www.googleapis.com/drive/v3/files/{doc_id}/permissions?sendNotificationEmail=false",
            data=json.dumps({
                "role": "writer",
                "type": "user",
                "emailAddress": PERSONAL_EMAIL
            }).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
        )
        safe_urlopen(perm_personal)
        print(f"👤 Permiso de edición otorgado a la cuenta personal: {PERSONAL_EMAIL}")
    except Exception as e:
        print(f"⚠️ Nota permiso personal: {e}")

    try:
        perm_anyone = urllib.request.Request(
            f"https://www.googleapis.com/drive/v3/files/{doc_id}/permissions",
            data=json.dumps({"role": "reader", "type": "anyone"}).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
        )
        safe_urlopen(perm_anyone)
        print("🌍 Permiso de lectura pública por enlace habilitado.")
    except Exception as e:
        print(f"⚠️ Nota permiso público: {e}")

    doc_url = f"https://docs.google.com/document/d/{doc_id}/edit"
    print(f"👉 URL Oficial: {doc_url}")
    return doc_url, doc_id

if __name__ == "__main__":
    token = get_access_token()
    url, doc_id = create_google_doc(token)
    print(f"DOC_URL={url}")
