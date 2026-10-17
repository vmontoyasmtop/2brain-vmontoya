#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Oficial ALFRED / Docs Expert:
Creación del Documento Oficial de Google Docs del Sermón 2:
"La Paz en Medio de la Tormenta" (Estudio Exegético & Manuscrito de Púlpito).
Formato limpio y optimizado para estudio y atril (Púlpito / Tablet / Impresión).
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

def build_printable_content():
    return """================================================================================
SERMÓN 2: LA PAZ EN MEDIO DE LA TORMENTA
Serie de Sermones: Jesús, Solución a Todo Problema (Filipenses 4:13)
Guía Integral de Estudio Exegético & Manuscrito Homilético para Púlpito
================================================================================

PASAJES BÍBLICOS CLAVE:
• Marcos 4:35-41 (Texto Principal de Exposición)
• Juan 14:27 — «La paz os dejo, mi paz os doy; yo no os la doy como el mundo la da.»
• Filipenses 4:6-7, 13 — «Y la paz de Dios... guardará vuestros corazones... Todo lo puedo en Cristo que me fortalece.»
• Hechos 27:21-25 — «Tened buen ánimo, porque yo confío en Dios...»

PROPOSICIÓN CENTRAL (BIG IDEA):
"La paz que Jesús imparte no es la ausencia de tormentas a nuestro alrededor, sino la presencia viva del Salvador gobernando nuestra barca; Su poder nos capacita para no quebrarnos ante ninguna crisis de este mundo."

DURACIÓN ESTIMADA: 40 a 45 minutos
TONO: Pastoral, cinematográfico en la narración, doctrinalmente sólido y consolador.

================================================================================
PARTE I: ESTUDIO EXEGÉTICO & LINGÜÍSTICO (GRIEGO BÍBLICO)
================================================================================

1. LAILAPS MEGÁLĒ (λαῖλαψ μεγάλη — Marcos 4:37)
   • Traducción: Gran tempestad de viento / Turbión ciclónico.
   • Trasfondo: El Mar de Galilea está a ~210 m bajo el nivel del mar, flanqueado por los cañones del Hermón. El choque de aire frío con el calor del valle desata vendavales rotativos feroces.
   • Significado: No es un chubasco común (hyetos), sino un torbellino violento que hace girar las aguas en espiral. Cuatro pescadores veteranos (Pedro, Andrés, Jacobo, Juan) estaban aterrorizados porque la crisis desbordaba toda pericia técnica humana.

2. KATHEÚDŌN EPÌ TÒ PROSKEPHÁLAION (καθεύδων ἐπὶ τὸ προσκεφάλαιον — Marcos 4:38)
   • Traducción: Durmiendo en la popa sobre el cabezal.
   • Detalle Histórico: La popa era el lugar del timonel; el cabezal de cuero acolchado servía para gobernar la nave.
   • Teología de Cristo: Revela Su perfecta humanidad (cansancio físico tras predicar y ministrar) y Su perfecta confianza filial en la providencia del Padre (Salmo 4:8).

3. SIŌPA, PEPHÍMŌSO (Σιώπα, πεφίμωσο — Marcos 4:39)
   • Traducción: «¡Calla, sé amordazado y permanece enmudecido!»
   • Análisis Gramatical: Siōpa (imperativo presente activo: silencio inmediato y continuo); Pephímōso (imperativo perfecto pasivo de phimoō: amordazar con bozal y sellar para siempre).
   • Autoridad Cósmica: Jesús no suplica al viento; habla como el Creador de Génesis 1 y Job 38:11.

4. GALĒNĒ MEGÁLĒ (γαλήνη μεγάλη — Marcos 4:39)
   • Traducción: Gran bonanza / Calma sobrenatural.
   • Contraste Divino: Frente a la «gran tormenta» (lailaps megalē), la palabra de Cristo desata una «gran calma» (galēnē megalē). El oleaje no tardó horas en amortiguarse; las aguas quedaron como un cristal pulido instantáneamente.

5. PHROURĒSEI (φρουρήσει — Filipenses 4:7)
   • Traducción: «Guardará / Custodiará».
   • Contexto Militar: Describe una guarnición o pelotón romano apostado a las puertas de una fortaleza. La paz de Dios es un centinela armado que impide la entrada del pánico al corazón.

6. ENDYNAMOUNTI (ἐνδυναμοῦντι — Filipenses 4:13)
   • Traducción: «En Aquel que continuamente infunde dinamismo y poder interior».
   • Verdad Central: No es autosuficiencia humana («yo puedo lograr todo lo que me proponga»), sino la suficiencia divina para resistir y cruzar cualquier tempestad terrenal.

================================================================================
PARTE II: FICHA DE ESTRUCTURA HOMILÉTICA
================================================================================

EJE DE LOS TRES PUNTOS:
• Punto 1: Tormentas en el Camino de la Obediencia (Marcos 4:35-37)
• Punto 2: El Descanso del Soberano vs. El Pánico del Hombre (Marcos 4:38-40)
• Punto 3: La Autoridad de Cristo: Calmar el Viento o Sostener al Discípulo (Marcos 4:39; Hechos 27:21-25; Filipenses 4:7, 13)

INDICADORES PARA EL ATRIL:
• [PAUSA - SILENCIO] : Detenerse 3 a 4 segundos. Mirar a la congregación.
• [VOZ CERCANA]     : Tono cálido, íntimo y pastoral; hablar al corazón afligido.
• [ÉNFASIS FIRME]   : Voz con autoridad espiritual, firmeza y convicción.
• [NARRACIÓN GRÁFICA]: Pintar el cuadro bíblico cinematográficamente.
• [INTERACCIÓN]     : Pregunta reflexiva para conectar vivencias del pueblo.

================================================================================
PARTE III: MANUSCRITO COMPLETO DE PÚLPITO
================================================================================

1. APERTURA E INTRODUCCIÓN (0:00 - 8:00)
--------------------------------------------------------------------------------
[VOZ CERCANA]
Iglesia amada, qué gozo verlos hoy en la casa del Señor. La semana pasada dimos inicio formal a nuestra serie: "Jesús: Solución a Todo Problema". Aprendimos el secreto que el apóstol Pablo descubrió en una celda romana: el contentamiento sagrado; descubrimos que el afán divide nuestra mente, pero que estar en Cristo nos da la plenitud interior independientemente de lo que tengamos o nos falte en el bolsillo.

Pero hoy debemos dar un paso más profundo. Porque una cosa es aprender a estar contentos cuando los planes tardan... y otra muy distinta es cuando la vida de repente nos parte en dos con una tormenta violenta que no vimos venir.

[INTERACCIÓN]
¿Cuántos de los presentes han tenido alguna vez uno de esos días donde se levantaron con el cielo despejado, todo marchaba en orden... y a las tres de la tarde una llamada telefónica, un diagnóstico del laboratorio, una carta de despido o una noticia familiar les sacudió el piso por completo?

[PAUSA - SILENCIO]

Todos hemos estado allí. Todos sabemos lo que se siente cuando el agua empieza a entrar en la barca más rápido de lo que podemos achicarla con nuestras manos cansadas.

[VOZ CERCANA]
Vivimos en un mundo obsesionado con la tranquilidad. La gente paga fortunas buscando lo que llaman "un poco de paz". Pero escúchenme bien: la paz que este mundo ofrece es frágil y barata porque depende exclusivamente de que no haya olas. El mundo dice: "Tendrás paz cuando pagues todas tus deudas, cuando sanes de todas tus dolencias y cuando nadie te critique". En otras palabras: el mundo te promete paz para un planeta utópico que no existe.

Pero Jesús no vino a darnos esa paz cosmética. Jesús dijo en Juan 14:27:
«La paz os dejo, mi paz os doy; yo no os la doy como el mundo la da. No se turbe vuestro corazón, ni tenga miedo.»

Hoy vamos a abrir la Palabra en el Evangelio de Marcos, capítulo 4, versículos 35 al 41.

--------------------------------------------------------------------------------
2. LECTURA BÍBLICA PRINCIPAL (Marcos 4:35-41)
--------------------------------------------------------------------------------
«35 Aquel día, cuando llegó la noche, les dijo: Pasemos al otro lado.
 36 Y despidiendo a la multitud, le tomaron como estaba, en la barca; y había también con él otras barcas.
 37 Pero se levantó una gran tempestad de viento, y echaba las olas en la barca, de tal manera que ya se anegaba.
 38 Y él estaba en la popa, durmiendo sobre un cabezal; y le despertaron, y le dijeron: Maestro, ¿no tienes cuidado que perecemos?
 39 Y levantándose, reprendió al viento, y dijo al mar: Calla, enmudece. Y cesó el viento, y se hizo grande bonanza.
 40 Y les dijo: ¿Por qué estáis así amedrentados? ¿Cómo no tenéis fe?
 41 Entonces temieron con gran temor, y se decían el uno al otro: ¿Quién es este, que aun el viento y el mar le obedecen?»

Oración de Iluminación:
«Padre eterno, te pedimos que en esta mañana la voz que amordazó al viento y al mar hable al corazón de cada persona atribulada en este lugar. Que caigan las vendas del pánico, que se desarticule el espíritu de queja y que tu paz sobrenatural monte guardia en nuestras mentes y corazones en Cristo Jesús. Amén.»

--------------------------------------------------------------------------------
3. PUNTO 1: TORMENTAS EN EL CAMINO DE LA OBEDIENCIA (8:00 - 18:00)
--------------------------------------------------------------------------------
[NARRACIÓN GRÁFICA]
Miren con atención el versículo 35. ¿Quién tomó la iniciativa de subir a la barca y cruzar el lago?
No fue Pedro. No fue Juan. El texto dice: «Aquel día, cuando llegó la noche, LES DIJO: Pasemos al otro lado».

[ÉNFASIS FIRME]
¡Fue Jesús quien dio la orden! Fue el Maestro quien trazó la ruta hacia la otra orilla.

Muchos creyentes arrastran lo que podríamos llamar el "síndrome de Jonás". Cuando les sobreviene una prueba grave, inmediatamente se torturan diciendo: "¿Qué pecado habré cometido? ¿Por qué Dios me estará castigando?".
Y es verdad: Jonás estuvo en medio de una tormenta porque estaba huyendo de Dios. ¡Pero los discípulos de Marcos 4 estaban en medio de una tormenta brutal precisamente por obedecer a Dios al pie de la letra!

[VOZ CERCANA]
Estar en el centro de la voluntad de Dios no significa navegar en un estanque de aguas mansas. Jesús nunca te prometió un pase libre de adversidades. Lo que te prometió en Juan 16:33 fue: «En el mundo tendréis aflicción; pero confiad, yo he vencido al mundo».

[ÉNFASIS FIRME]
Si hombres curtidos en el mar como Pedro y Andrés estaban desesperados, era porque la fuerza del agua superaba toda pericia técnica.
Tal vez hoy tú estás diciendo: "Pastor, he sido honrado, he servido al Señor... ¿por qué estoy viviendo esta tormenta?".
Escucha esta verdad: La tormenta no significa que tomaste el camino equivocado; la tormenta significa que estás cruzando al otro lado bajo la orden del Rey. Y la palabra de Jesús («Pasemos al otro lado») tiene más peso que todo el viento del infierno.

--------------------------------------------------------------------------------
4. PUNTO 2: EL DESCANSO DEL SOBERANO vs. EL PÁNICO DEL HOMBRE (18:00 - 28:00)
--------------------------------------------------------------------------------
[NARRACIÓN GRÁFICA]
Contemplen el contraste del versículo 38. Afuera: relámpagos, el viento rugiendo, las olas golpeando con violencia, los discípulos empapados gritando y achicando agua...
Y en la popa, sobre el cabezal de cuero reservado para el timonel: ¡Jesús, durmiendo profundamente!

[PAUSA - SILENCIO]

Vemos Su verdadera humanidad: exhausto tras largas horas de prédica y ministerio. Pero también vemos Su perfecto descanso filial en el Padre. Jesús no tenía que desvelarse angustiado porque sabía quién gobernaba los cielos y sostenía Su vida.

[VOZ CERCANA]
¿Y qué hicieron los discípulos? Fueron a la popa, lo sacudieron con violencia y le lanzaron esa pregunta tan humana:
«Maestro, ¿no tienes cuidado que perecemos?» (¿No te importa que nos ahoguemos?).

¿Alguna vez le has hecho esa pregunta a Dios en el secreto de tu habitación?
- "Señor, ¿no ves que mi matrimonio se está hundiendo?"
- "Señor, ¿no te importa el dolor de este diagnóstico médico?"
- "Señor, ¿no te das cuenta de que el dinero no me alcanza y tú pareces guardar silencio?"

Los discípulos no pecaron por sentir miedo ante olas descomunales. Pecaron cuando permitieron que el miedo pusiera en duda el amor y el carácter de Jesús. El miedo siempre susurra la mentira del enemigo: "A Dios no le importas".

[ÉNFASIS FIRME]
¡Pero Jesús estaba en la misma barca que ellos! Si la barca se hundía, Jesús se hundía con ellos. ¡Era imposible que perecieran llevando a bordo al Creador del universo!
Hermanos amados: Jesús puede parecer dormido en tu circunstancia, pero jamás está ausente. Su aparente silencio no es indiferencia; es el taller donde se entrena y se purifica la fe.

--------------------------------------------------------------------------------
5. PUNTO 3: LA AUTORIDAD DE CRISTO: CALMAR EL VIENTO O SOSTENER AL DISCÍPULO (28:00 - 38:00)
--------------------------------------------------------------------------------
[ÉNFASIS FIRME]
En el versículo 39, Jesús se pone en pie en medio de la barca. No hace ritos mágicos ni aspavientos. Mira al viento tempestuoso y al mar enfurecido y pronuncia:
«¡Siōpa, pephímōso!» (¡Calla, sé amordazado y permanece en silencio!).
Y al instante sobrevino una gran bonanza. El mar quedó liso como un espejo de cristal.

[VOZ CERCANA]
Muchos buscan en Cristo únicamente a un "apagador de tormentas": "Señor, quítame este problema de encima". Y gloria a Dios porque Jesús puede disipar cualquier tormenta en un milisegundo si es Su voluntad.

Pero, ¿qué sucede cuando la tormenta no cesa al instante? ¿Qué sucede cuando el tratamiento médico se alarga? ¿Significa que Jesús te abandonó?

[ÉNFASIS FIRME]
¡De ninguna manera! Porque hay un milagro aún mayor que calmar la tormenta externa: y es cuando Jesús permite que la tormenta siga rugiendo afuera, pero calma el corazón del creyente por dentro.

Eso fue lo que vivió el apóstol Pablo en Hechos 27. Catorce días en un barco azotado por una tempestad huracanada en el Mediterráneo, sin ver el sol ni las estrellas. Todos daban por perdida su vida. Pero Pablo se puso en pie en medio de la noche, tomó pan, dio gracias a Dios y les dijo:
«Tened buen ánimo, porque yo confío en Dios que será así como se me ha dicho. Ninguna vida se perderá.»

¿De dónde sacaba Pablo esa serenidad? De Filipenses 4:6-7:
«Y la paz de Dios, que sobrepasa todo entendimiento, guardará vuestros corazones y vuestros pensamientos en Cristo Jesús.»
La palabra "guardará" (phrourēsei) describe a una guarnición militar romana montando guardia día y noche en tu corazón para que el pánico no pueda entrar.

Y remata en Filipenses 4:13:
«¡Todo lo puedo en Cristo que me fortalece!»
No significa "todo lo puedo conquistar en mis fuerzas", sino: ¡Tengo el poder de Cristo para atravesar esta tormenta con dignidad, con fe y con gozo, porque el Señor va conmigo en la barca!

--------------------------------------------------------------------------------
6. CONCLUSIÓN & LLAMADO AL ALTAR (38:00 - 45:00)
--------------------------------------------------------------------------------
[VOZ CERCANA]
Amada congregación, resumamos esta enseñanza en tres verdades para el corazón:
1. La tormenta no invalida la orden de Dios: Si Jesús dijo «pasemos al otro lado», vas a llegar.
2. Desarma la queja acusadora: Si Dios entregó a Su propio Hijo en la cruz, jamás dudes de Su amor.
3. Entrega el timón: La verdadera paz no es la ausencia de olas, es la presencia del Rey gobernando tu barca.

[PAUSA - SILENCIO]

Invitación al Altar (Música instrumental suave):
Hoy quiero hablarle a la persona, al matrimonio, a la familia que siente que el agua le ha llegado al cuello.
A quienes han perdido el sueño por una crisis financiera.
A quienes enfrentan un diagnóstico que los llenó de zozobra.
A quienes sienten que las olas de la tensión están a punto de volcar su hogar.

El Señor te trajo hoy aquí para decirte: ¡No estás solo en la barca!
Si necesitas que la paz de Dios monte guardia en tu mente y quieres decirle a Jesús: "Toma el timón de mi vida", te invito a pasar a este altar ahora mismo.

Oración de Ministración:
«Señor Jesús, hoy reconozco que he mirado demasiado la altura de las olas y la fuerza del viento.
Perdóname si en momentos de angustia dudé de tu cuidado y pensé que no te importaba mi dolor.
Hoy te entrego el timón absoluto de mi vida.
Sujeto mis emociones, mis pensamientos y mis finanzas bajo tu señorío.
Y en el nombre de Jesús le digo al espíritu de angustia: ¡Calla, enmudece!
Recibo tu paz sobrenatural que sobrepasa todo entendimiento.
Declaro sobre mi vida y sobre mi hogar: ¡Todo lo puedo en Cristo que me fortalece!
No me voy a hundir, porque mi Salvador va en mi barca.
En el nombre poderoso de Jesús, ¡Amén!»
================================================================================
"""

def create_google_doc(access_token):
    title = "⛪ SERMÓN 2: La Paz en Medio de la Tormenta (Estudio & Púlpito)"
    
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

    # 2. Insertar texto formateado
    content = build_printable_content()
    requests = [{
        "insertText": {
            "location": {"index": 1},
            "text": content
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

    # 3. Otorgar permisos a la cuenta personal (vmontoya.smartopsve@gmail.com) como editor y a cualquiera con el link como lector
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
