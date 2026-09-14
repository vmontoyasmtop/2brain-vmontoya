---
title: "Google Lanzó Antigravity CLI y Es Brutal"
source: "https://www.youtube.com/watch?v=bdEqIchP4x4&list=PLZuFQuIouebI&index=5"
author:
  - "[[Fazt Code]]"
published: 2026-05-21
created: 2026-09-11
description: "🔥 Despliega tus proyectos fácilmente 👉 https://seenode.com✅ Aquí tienes una descripción optimizada para YouTube:Antigravity CLI: El Nuevo Agente de Google que Está Rompiéndola en 2026Google aca"
tags:
  - "clippings"
---
![](https://www.youtube.com/watch?v=bdEqIchP4x4)

🔥 Despliega tus proyectos fácilmente 👉 https://seenode.com  
  
✅ Aquí tienes una descripción optimizada para YouTube:  
  
Antigravity CLI: El Nuevo Agente de Google que Está Rompiéndola en 2026  
Google acaba de lanzar Antigravity CLI, un nuevo agente de IA escrito completamente en Go, ultrarrápido y que puedes usar gratis con tu cuenta de Google. En este video te muestro una review completa + tutorial paso a paso de todo lo que puede hacer.  
Lo que verás en el video:  
  
Cómo instalar Antigravity CLI en Windows, Mac y Linux  
Autenticación y uso con Gemini 3.5 Flash (plan gratuito)  
Creación de aplicaciones completas (Frontend + Backend) en minutos  
Modo Planning y creación de planes detallados  
Subagentes (Research Agent + Tester Agent)  
Skills (instalación de Frontend Design de Anthropic)  
Comandos útiles: /artifact, /planning, /bytheway, /rewind, /goal, /task, etc.  
Comparación de velocidad vs Cursor y Claude Code  
Uso de múltiples modelos (Gemini, Claude, GPT open source)  
  
Antigravity CLI combina velocidad brutal, una interfaz muy limpia y características avanzadas que lo posicionan como uno de los mejores agentes de código del momento.  
¿Cursor o Antigravity? En este video te doy mi opinión sincera después de probarlo a fondo.  
  
🔗 Enlaces importantes:  
  
Instalación de Antigravity CLI → https://antigravity.google/download  
  
Indice:  
00:00 Introducción: ¿Qué es Antigravity CLI?  
00:45 Patrocinio  
01:51 Instalación de Antigravity CLI  
02:23 Autenticación con cuenta de Google  
03:02 Configuración inicial (tema y permisos)  
03:43 Reanudar sesión con agi -c  
03:58 Primera prueba: crear app de gestión de proyectos  
04:38 Comando /artifact (historial de cambios)  
04:48 Implementar dark/light mode  
05:01 Comando /btw (by the way)  
05:50 Configurar permisos y modo Yolo  
06:16 Generar versión en React  
07:10 Modo plan con /planning  
09:11 Cambiar entre modelos (/model)  
10:00 Gestionar procesos con /tasks  
11:55 Ver consumo con /usage  
12:30 Ver contexto disponible con /context  
13:00 Volver a sesiones previas con /rewind  
13:53 Limpiar contexto con /clear  
13:59 Modo bash con #  
14:43 Atajos de teclado y nueva línea (Ctrl+Enter)  
15:30 Editar planificaciones con comentarios  
16:51 Comandos slash disponibles  
17:53 Comando /goal (iteración automática)  
18:58 Instalar Skills (frontend-design)  
20:48 Crear y usar subagentes (/agents)  
23:00 Activar notificaciones  
23:34 Conclusiones y opiniones finales  
  
Si te gustó el video dale Like, suscríbete y activa la campanita para más contenido de desarrollo e IA.  
¿Quieres que haga un curso completo de Antigravity CLI? Déjamelo en los comentarios.

## Transcript

### Introducción: ¿Qué es Antigravity CLI?

**0:00** · El día de ayer, Google lanzó un nuevo agente de día llamado Antigravity Clive, que en teoría es la continuación de lo que sería Gemini Clive. Y aunque parecería simplemente un cambio de nombre, algo muy interesante es que han recreado el agente desde cero. De hecho, este nuevo agente está escrito en Go, responde muy rápido y sobre todo también pueden utilizarlo gratuitamente con un plan de Google. Entonces, justo ahora ustedes pueden utilizar los modelos de Google como Opus e incluso hasta una versión open source de GPT.

**0:21** · Pero bueno, para saber todo lo que hace este nuevo agente que es Antigravity CLI, el día de hoy les voy a mostrar un paso a paso de todo lo nuevo y también pueden verlo en la práctica qué tamban bien funciona en cuanto a respuestas y modos de uso porque tiene algunas cosas nuevas interesantes y si lo comparamos con CloudCe en ese caso ya tiene algunas características que se le parecen en algo. Así que si quieren ver un nuevo agente y sobre todo que pueden probar gratuitamente, este video les puede interesar. Vamos a empezar.

### Patrocinio

**0:45** · Coders, antes de empezar, si quieren desplegar una web completa que quizás han desarrollado con Note 10, Python, Go o incluso Elixir, más una base de datos, quizás PGRES o my SQL y quieren subirlo todo a un buen precio, deben conocer Cynote. Esta es una plataforma que te permite subir proyectos web de una forma muy simple y a un buen precio. Usarlo es muy fácil, solo conectas tu repositorio de GitHub o Gitlab, eliges tu proyecto y en segundos tu aplicación ya está en línea con una URL pública lista para usarse. Además, la plataforma ya incluye el esencial como permitirte añadir un dominio personalizado. Ya le añade https y también te da lo en tiempo real.

**1:17** · Tiene soporte también para wet sockets y http2. Añadir variables de entorno y tiene un soporte 247. Y en cuanto a precios puedes desplegar base de datos de Postres o MySQL desde $4 al mes y servidores backend desde $ al mes. Con esto ya tendrías tanto tu frontend y backen funcionando en producción. Así que para proyectos pequeños, MVPs o clientes con bajo presupuesto, esta es una opción rápida, simple y económica. Y si en caso quieres probar la plataforma antes, también tienes un trial gratuito de 7 días para que puedas subir tu proyecto.

**1:48** · Para saber más de Cynote, te dejo un enlace en la descripción. Muy bien, para empezar a utilizar Antigravity en su versión CLI o versión de consola, pues simplemente le voy a dejar el enlace en la descripción. E instalarlo es muy sencillo porque ya tiene un comando especial para tanto Windows, Mac y Linux. Entonces, en mi caso estoy en Windows el día de hoy. Voy a copiar esto de aquí. esta dirección.

### Instalación de Antigravity CLI

**2:05** · Luego vamos a venir en una terminal y simplemente lo pegamos. Y bueno, si esperamos un poco vamos a ver un mensaje como este, que ahora ya tenemos Antigravity Cli disponible y nos dan un comando que se llama agi, que es un abreviado de antigravity. Entonces, simplemente escribimos ahí, pero es muy importante que aquí al menos en Windows, pues reinician la terminal y ahora sí, si escriben a pues van a ver esta bienvenida de antigravity. Ahora, muy importante, cuando empiezan a utilizarlo tienen dos formas de poder tener en los modelos de Google. La primera es con una autenticación con su cuenta y lo otro es crearse un proyecto en Google Cloud y a partir de allí pueden consumir tokens directamente de su API.

### Autenticación con cuenta de Google

**2:33** · Pero si ustedes son desarrolladores y quieren pagar una suscripción, el Google Authentication es lo que ustedes irían. Entonces vamos por la número uno. Aquí me pide que entre en esta dirección. Simplemente vamos a abrirlo en un navegador y a partir de aquí me va a pedir autorización y simplemente le damos en acceder. Y por cierto, como la salida puede ser algo extensa, también pueden presionar shift y arriba y hacia abajo y pueden ver que pueden hacer scroll aquí dentro de este agente. Y bueno, lo que me pide es que coloque el código. Entonces aquí me va a dar un código. Vamos a pegarlo allí.

**2:58** · Damos un enter y listo. Ahora ya estoy dentro de Antigravity. Ya podemos cerrar esta ventana. Entonces, lo primero que vemos es que tenemos algunos temas. Por ejemplo, hay algunos que se ven mucho mejor que otros. En mi caso, voy a escoger simplemente el tema dark. Vamos a aceptar los permisos primero alejándonos un poco y vamos a darle en don't. Y aquí me dice que Antigravity requiere permisos para leer y ejecutar dentro de esta carpeta donde estoy ubicado. Entonces, de momento voy a decirle, sí, confío en este folder y a partir de allí lo que vamos a ver es algo como esto. Tenemos un hola, soy Antigravity y tu asistente en programación. ¿En qué puede ayudarte hoy? Ahora, algo beneficioso que estoy notando con esta gente es que realmente retorna muy rápido la respuestas, no solamente por el modelo, es decir, sino a la sensación de ejecutar comandos.

### Configuración inicial (tema y permisos)

**3:29** · Es decir, si ustedes escriben un slash, pueden ver que todo es prácticamente instantáneo. Ahora, esto no parecería mucho, pero yo he probado cloud code o mejor dicho, uso Cloud Code todos los días y Codex también. Y sí se nota la experiencia en ese caso, al menos que es código nativo. Es decir, esto está escrito en Go. Y por cierto, también ha añadido este comando para poder reanudar una sesión. Es decir, si ustedes quieren volver una sesión que ya habían escrito antes, al igual que en Cloud Code, tienen este comando llamado gu-c, es decir, si quieren ejecutarlo nuevamente o reanudar su sesión, simplemente escriben agi-c y con eso vuelven al chat que ya habían chateado algo antes.

### Reanudar sesión con agi -c

### Primera prueba: crear app de gestión de proyectos

**3:58** · Entonces, vamos a empezar probando algo muy sencillo y en este caso le voy a pedir algo como esto. Le voy a decir, "Crea un app para administrar proyectos con una vista canvant." Y lo típico que me dice si quiero aceptar la ejecución de comando, vamos a decirle que sí. Y bueno, si esperamos un poco, lo que vamos a ver es algo como esto. Tenemos una salida que en lo personal lo veo bastante ordenado, es decir, tenemos la ejecución de los comandos, las tareas que he ido completando y esto se ve bastante bien, al menos para leerlo o saber qué es lo que hizo la IA.

**4:19** · Y también algo genial es que muy aparte de tener los enlaces aquí para abrir directamente el sitio, que de hecho, por ejemplo, tendríamos que ejecutar esto en el local house 5173 o simplemente dar un click y van a ver que aquí está la aplicación que acaba de crear. Es una aplicación muy sencilla y como pueden ver no luce nada mal. Ahora, si lo notan también tiene un comando llamado Slash Artifact que si lo escribimos aquí lo que va a hacer este comando es como una lista de justamente todas las modificaciones que hizo. Es decir, en este caso solo tenemos una que es la planificación, pero bueno, si nosotros empezamos a pedir más, pues allí se genera como un historial. Ahora vamos a pedir algo más, por ejemplo, que implemente el dark mode y light mode.

### Comando /artifact (historial de cambios)

### Implementar dark/light mode

**4:51** · Por ejemplo, le digo, implementa un dark light team. Y en este caso responde bastante bien. Y por cierto, al igual que en CloudCode, nosotros ahora también tenemos un comando llamado slash by the way o slbtw que lo que hace es que nosotros podemos ir preguntando cosas a medida que se va haciendo algo. Pero bueno, en este caso lo ha hecho demasiado rápido y bueno, si lo revisamos, esto es lo que ha hecho y no lo sé tampoco nada mal a pesar de ser el primer pronto. Ahora, si revisamos el código, lo que vamos a ver es que ha generado un archivo index HTML y es por eso que también todo lo ha generado rápido. Pero lo que vamos a pedir ahora es que genere, por ejemplo, la versión en React. Y si nosotros queremos probar ese comando, by the way, simplemente escribimos btw.

### Comando /btw (by the way)

**5:21** · Y aquí podríamos decirle, "¿Y qué estás utilizando para los estilos?" Y lo que va a hacer esto es que mientras está trabajando, por ejemplo, en la tarea que le he dado, aquí también nos puede ir respondiendo otras cosas. Es como lanzar una pregunta adicional que no interrumpe lo que está haciendo la guía. Obviamente, si ustedes quieren modificar las respuestas, pues simplemente lo escriben y dan un enter y ya. Pero el by the way es para que nos responda algo a medida que la gente ya viene trabajando en otras cosas. En ese caso es un poco molesto cuando ustedes están desarrollando que cada minuto le esté preguntando algo. Así que obviamente también lo pueden cambiar. Si escriben slashcig y dan un enter, lo que van a ver aquí es todas las configuraciones básicas del editor.

### Configurar permisos y modo Yolo

**5:51** · Y lo que nos interesa en este momento es esta opción que se llama tool permission. D un enter y aquí, por ejemplo, está actualmente en pregúntame en cada revisión. Ahora vamos a decirle always proceed o siempre procede para que ya no nos pregunte a cada momento en cada modificación. Ese es el yolo mode o el pasar los permisos simplemente por parte de la IA. Entonces, esa es la forma en la que típicamente van a necesitar configurarlo. Y bueno, pueden presionar escape y ya con eso salen de la configuración y pueden ver que aquí al parecer ya terminó de reescribirlo. Me dice, "Okay, hay un componente principal y bueno, aquí me da el resumen, me dice, puedes ejecutarlo en el 5174." Damos un clic allí.

### Generar versión en React

**6:21** · Sí, al parecer esta es la misma aplicación y no se ve nada mal, de hecho, hasta veo que tiene una aquí que otra animación adicional, pero vamos a revisar el código. Y lo que ha hecho es crear otro proyecto por aparte, es decir, no ha reescrito en el mismo lugar, lo cual es una buena idea, de hecho, porque otra idea lo que hubiera hecho es crear todo el proyecto desde cero o eliminarlo, pero en este caso ha creado otro proyecto por aparte que se llama Canan React y este es el que estamos viendo. Y bueno, si revisamos su código, van a ver que aquí es una aplicación de React, simplemente con código allí de demo, es decir, todo es puro frontend al final.

**6:48** · Pero esto obviamente tiene algunas ventajas porque ahora nosotros ya podríamos empezar a comunicarlo con algún tipo de backend y podríamos accenderlo mucho más fácilmente o hacerlo crecer más el proyecto. Pero bueno, aquí pueden ver que es un proyecto de PJS. Ahora, al igual que en CloudC, cada cierto tiempo te aparece estos mensajes de poder calificar, por ejemplo, uno para bien, dos para más o menos y tres para malo.

**7:06** · En este caso, vamos a colocarle uno y bueno, va avanzando bastante bien realmente. Ahora, si ustedes quieren también armar una planificación y no solamente hacer by coding, es decir, no quieren pasar solamente escribiendo y pidiendo cosas, sino que quieren pedirle una modificación muy grande, también pueden entrar en el modo plan. De hecho, aquí no es con un Shift tab al igual que en otros agentes como Cloud Code o Codex, sino que aquí escriben slash planning y dan un tab, se autocompleta y dan un enter. Y aquí van a ver un mensaje como este que dice planning mode habilitado. Eso quiere decir que ahora ya podrían pedir una planificación. Por ejemplo, le voy a decir implementa un backend en hono con band y una base de datos de SQLite.

### Modo plan con /planning

**7:39** · Y lo que voy a empezar a hacer aquí es justamente primero una verificación. estaba comprobando que van esté escrito, está creando una tarea primero y esta forma de ver los cambios, como pueden ver, es mucho más cómoda, es decir, puedo ir viendo de forma resumida qué es lo que está haciendo y no veo todos los mensajes amontonados como pasa en otros agentes. Entonces, esta forma ordenada de resumirlos me parece mucho más sensato y es mucho mejor porque al final obtenemos el resultado que es un mensaje mucho más descriptivo y es lo que nos interesa al final.

**8:04** · Y bueno, aquí me dice backend hono más band, aunque en este caso, de hecho, aquí a pesar de que me dice planning habilitado, eh, no le ha creado la planificación, sino que ya hizo el cambio. Entonces, vamos a probarlo nuevamente. Voy a pedir de esta forma, crea un plan para implementar autenticación en la API con Jason Web Token. Y ahora sí, lo que está haciendo es crear el plan. Es un poco curioso porque si bien aquí me dice que entró en el modo plan al pedirlo la primera vez como simplemente le dije implementa un backend, pues lo entendió cómo hacerlo.

**8:30** · Aquí le he dicho crea un plan literalmente y ya con eso ha creado un archivo llamado implementationplan out.

**8:36** · Que es justamente lo que está aquí. Y bueno, ahora sí, sin saltar a ningún modo plan, le digo, impléntalo. Y con esto, pues como hemos visto antes, va a empezar a hacer las modificaciones.

**8:44** · Ahora, aquí ya lo implementó y de hecho me dice backen con h no frontend. Vamos a probarlo. En este caso, simplemente vamos a entrar en la aplicación y bueno, ahora tengo un login y bueno, si aquí pruebo con un usuario como T, este es un 23, por ejemplo, me dice, "Okay, registro exitoso, por favor in sesión, aunque allí lo deja en rojo, así que podría interpretarse como un error, pero bueno, esta es la aplicación y ahora debería tener un logout. Entonces, si vuelvo a entrar como t es 1 2 3, pueden ver que nuevamente puedo ingresar."

**9:06** · Bueno, de forma resumida, al menos la experiencia que estoy obteniendo es que es muy rápido, aunque bueno, en realidad también es por el modelo que estoy utilizando y es que si nosotros escribimos las model, por ejemplo, y damos un enter, pueden ver que el modelo que estoy utilizando de momento es Gemini 3.5 Flash. Por cierto, aquí yo no tengo ninguna suscripción, así que estoy utilizando el plan gratuito. Obviamente, si esto les responde muy bien, pues podrían considerar pagar el plan Pro o el plan pagado de Google, pero bueno, estoy justamente con el modelo más rápido y obviamente también pueden ir cambiándolo entre modelos. Por ejemplo, aquí también algo muy interesante es que al igual como pasa en Antigravity, también tienen acceso a los modelos por parte de otras empresas.

### Cambiar entre modelos (/model)

**9:37** · Por ejemplo, tienen Cloudset, ya sea en versión Thinking y Cloud Opus también en versión Thinking. E incluso tienen una versión de GPT open source, pero bueno, con esto es tan fácil como seleccionar otro modelo, que en este caso, por ejemplo, si quieren un modelo que razone mucho mejor o haga tareas mucho mejor, pueden ir a 3.5 flash en su versión low y esto debería responder de igual forma. Ahora, en esta sesión he estado creando tres aplicaciones, una que es para back y dos de frontend. si recuerdan una en HTML y otra en React. Así que aquí también tiene un comando llamado slash task que pueden ejecutarlo y con eso van a ver la ejecución de los programas que tienen disponibles.

### Gestionar procesos con /tasks

**10:07** · Y bueno, aquí hay muchas salidas. Por ejemplo, al momento que hemos estado pidiendo cosas, pues la gente ha estado ejecutando una y otra vez uno que otro comando. Entonces, los que nos interesan de momento son estos marcados en amarillo porque están en versión running, es decir, son los programas del frontend y aquí también está el otro frontend. Y bueno, si bajamos un poco deberíamos encontrar el tercer programa y aquí está justamente el backend que es van run. Y bueno, para empezar a remover tareas de la lista, pueden escribir X, por ejemplo, voy escribiendo X y voy limpiando aquí algunos comandos, como pueden ver, bastante cómodo en realidad.

**10:36** · O si por ejemplo quieren terminar con un proceso que se está ejecutando porque quizás está consumiendo RAM o simplemente ya no usan ese proceso o esa tarea, pues pueden presionar letra K, como aquí también indica. Y por ejemplo, quiero acabar con la ejecución del primer proyecto, pero si lo notan, de hecho voy a limpiar un poco aquí entre tantos comandos. Vamos a ver que aquí tengo dos room de, entonces no sé cuál es el primer proyecto, pero podemos dar un enter. Entro en el primero y van a ver que aquí obtengo justamente un resumen y este es con bit, este es canvan re, ¿okay? Este no, un escape para salir.

**11:03** · Y luego aquí voy a ir en el primero y ese es el proyecto que no tiene salida, es básicamente un empn room de entonces ese es el que voy a eliminar. Entonces para terminar la tarea, simplemente presiono la letra K y listo, ya se canceló. X para limpiar y listo. De esta forma ya tengo solamente las dos tareas que estoy ejecutando y presión escape y listo. El proyecto debería seguir funcionando como antes. Por cierto, aquí nunca crea una tarea. Vamos a probarlo. Vamos a escribir una tarea de prueba. Se añade allí y sí, todo funciona bastante bien en realidad. Ahora, como ya tengo bastante historial, es decir, he pedido varias cosas, ahora sí podemos ver la ventaja de utilizar este comando artifact.

**11:33** · Y al dar un enter pueden ver que justamente están las dos planificaciones que ya he creado antes.

**11:38** · Aquí está implementation plan, que fue la primera y la que pedí de autenticación. Y aquí está plann out, por ejemplo, y puede entrar y aquí está el resumen de todo lo que he pedido.

**11:46** · Ahora, este es como un editor en línea, ¿ves? Solamente para ver el mardown, pero es bastante útil tener justamente la forma de revisar este tipo de planificaciones, sobre todo porque pueden llegar a ser bastante extensas.

### Ver consumo con /usage

**11:56** · Ahora, ya he pedido varias cosas, ¿cómo sé cuánto tengo disponible en mi cuenta?

**11:59** · Bueno, yo me he autenticado con un correo. Entonces, simplemente vamos a presionar escape aquí y vamos a escribir slashusage de esta forma. Y pueden ver que aquí, por ejemplo, me da como un resumen de lo que tengo disponible en modelos. De hecho es bastante para hacer simplemente un plan gratuito, aunque lo que me llama la atención es que todo básicamente está marcado como en verde, cuando en realidad ya he pedido cosas en 3.5 flash y demás, entonces es probable que esto aún no esté actualizado. Aquí ustedes pueden ver justamente a medida que se van acabando los modelos que van pidiendo.

**12:27** · Ahora, adicionalmente a eso, también podemos escribir slhcectext y esto al igual que en CloudCode, que también me parece muy acertado, es que han colocado esta forma de ver el contexto con cuadritos. Entonces, por ejemplo, los recuadros que están allí en gris significa el contexto disponibles que tenemos hasta ese momento, que como pueden ver es casi cerca de un millón. Y bueno, el restante pues se divide en herramientas del sistema y si lo que ya lleva el agente al momento que lo han creado, las herramientas que vienen incluidas en el agente. Y bueno, aquí incluso pueden obtener como una especie de resumen de lo que está haciendo. Por ejemplo, lo que está manteniendo también son los artifacts o los o las planificaciones que he pedido.

### Ver contexto disponible con /context

**12:58** · Y por cierto, también hay un comando que se llama slash rewind, que si presionamos escape y lo intentamos ejecutar como slash rewind de esta forma y damos un enter, lo que vamos a ver es una especie de navegación en historial para volver el código hacia atrás o simplemente establecer la sesión hacia atrás. Por ejemplo, supongamos que yo quiero volver al momento en el que solamente estaba el darlight in. Entonces, vamos a dar un enter y pueden ver que ahora ya estoy en esa sesión. Y esto también quiere decir que el código ha vuelto hacia atrás. Es por eso aquí también para la ejecución.

### Volver a sesiones previas con /rewind

**13:24** · Y de hecho, si nosotros escribimos rewind nuevamente, vamos a ver que hemos vuelto hacia atrás. Así que también tengan en cuenta que eso puede reescribir su historial, ¿okay? Pero bueno, eso es algo que tienen muchos agentes como CloudC también. Es decir, con este cambio de sesión, pues lo que he hecho es volver toda la sesión hacia atrás y ahora ya no está la aplicación de Read ni la de backend y así. Ahora, adicionalmente a esto, si ustedes por ejemplo quieren limpiar la sesión, pongamos tienen el contexto lleno, aunque en este caso, como pueden ver, tengo prácticamente todo el contexto disponible, pero supongo que quiero limpiarlo. También puede escribir el comando slash clear y vuelvo al inicio.

### Limpiar contexto con /clear

**13:53** · Entonces, esto es simplemente para limpiar el contexto en caso ustedes ya lo tengan muy lleno y quieren ahorrar tokens. Ahora, algo adicional que también a mí me gusta utilizar en los agentes es que también nosotros podemos ejecutar bash commands o comandos de la terminal. Por ejemplo, supongamos que yo quiero saber en qué carpeta estoy.

### Modo bash con

**14:07** · Bueno, en este caso yo sé que aquí la gente ya me lo dice, pero si yo escribo un símbolo de numeral, aquí pueden ver que me dice modo bash activado.

**14:13** · Entonces, puedo escribir PWD. Y bueno, aquí como estoy en un PowerSell, al parecer no se ejecuta, pero puedo ejecutar un eco, por ejemplo, y me dice eco Hello World, es decir, la ejecución de ese comando de allí. En realidad de eso es para que ustedes puedan ejecutarlo con Git. Por ejemplo, si ustedes van a escribir un Git de estatus, bueno, aquí me dice Git no es un repositorio, entonces esta es la forma para no saltar a otra terminal nueva y tratar de ejecutarlo. Pero bueno, esto lo hago en mi caso cuando tengo, por ejemplo, un historial muy largo y no quiero ir hacia arriba, simplemente entro en el modo numeral y escribo PWD. Y de esta forma nosotros podemos ir viendo justamente la salida de esos comandos.

**14:42** · De hecho, hablando de los comandos, también tienen el símbolo de interrogación que si tratan de escribirlo van a ver que aquí aparece una especie de resumen de todos los comandos que pueden ejecutar. Ahora, todos estos son atajos de teclado realmente para poder, por ejemplo, saltar dentro de una nueva línea. Por ejemplo, supongo que ustedes escriben, quiero la siguiente planificación y quieren saltar la siguiente línea.

### Atajos de teclado y nueva línea (Ctrl+Enter)

**14:59** · Si ustedes dan un enter, simplemente esto se va a enviar, pero si dan control enter, pueden ver que salta la siguiente línea y pueden decirle, eh, crea un backend en hono con SQL y van JGS, vamos a decirle control enter le digo el frontend debe ser react con bit y al dar un enter, pues allí es donde recién se envía, como pueden ver. Y bueno, en realidad yo no le he dicho de qué va la aplicación, así que esto me puede dar un error o dudas adicionales, aunque en este caso, por ejemplo, lo que me ha dado es esta implementación, que si doy un click, pueden ver que lo abre directamente con un editor de código y bueno, en realidad va bastante fluido.

### Editar planificaciones con comentarios

**15:30** · Entonces, si escribimos el Lash Artifact y doy un enter, también lo puedo revisar desde aquí. Y bueno, si nosotros por ejemplo queremos editar algo, aquí por ejemplo le puedo colocar un comentario, le puedo decir C y aquí le puedo comentar algo. Por ejemplo, le puedo decir la aplicación es para administrar finanzas personales. Damos un enter y ahora pueden ver que aquí arriba aparece como un texto adicionalmente en la planificación, es decir, a medida que nosotros vamos leyendo algo, podemos añadirle un comentario y luego la va a tomar de referencia a eso. Por ejemplo, aquí en el frontend con reividit, pues si bajamos un poco, vamos a ver que aquí me dice, "OK, componente principal y demás." Y le digo aquí un comentario y le digo, "Usa chat CN para la UI."

**16:01** · Doy un enter y se añadió el comentario y así podemos ir revisándolo, lo cual me parece también bastante acertado. Es muy fácil editarlo de esta forma. Entonces, vamos a dar un escape allí para saltar, pero aquí lo que van a ver es un mensaje que me dice, "Okay, tienes dos comentarios que no has establecido.

**16:16** · ¿Quieres enviarlo a la gente? Vamos a decir y listo. Ahora la gente va a tomar nuestra referencia de comentarios en la planificación y va a actualizar el plan." Entonces, aquí van a ver que me dice actualizado la planificación, hay cambios en el plan, por ejemplo, gestión de finanzas personales, frontend con chat y me dice, "Damos luz verde a la versión." Sí, vamos a decirle aquí, impleméntala y ya estaría. Y de nuevo, si nosotros quisiéramos ver eh la planificación final, también podemos escribir nuevamente slartifact y damos un enter y ahí justamente está la tarea que está implementando, que es la que ahorita justamente la gente está leyendo, y la otra es la planificación que ya habíamos visto.

**16:45** · Entonces, también podríamos entrar allí y revisarla nuevamente, es decir, añadir más comentarios. Ahora, algo adicional que ustedes también deberían conocer es el slash, que es básicamente para poder lanzar comandos. Y bueno, aquí hay algunos de los que ya les he mencionado.

### Comandos slash disponibles

**16:57** · Por ejemplo, está el slash model, que es para poder cambiar entre modelos, está el slash permission que es para poder darle acceso a las herramientas, slash planning, que ya hemos visto y por supuesto también tenemos el slash skills que si lo ejecutamos vamos a ver todos los skills que tenemos instalados, que de momento pues no tengo ninguno, pero pueden ver que justamente me dice que puedo añadirlos dentro de una carpeta punto skills y allí puedo colocar el nombre del skill. Ya lo vamos a hacer en breve, pero aquí básicamente con estos comandos pueden ver todo lo que puede hacer el agente.

**17:22** · De hecho tiene algunos bastante interesantes como el comando goal por ejemplo que es para poder lanzar una sesión y que la a puede iterar múltiples veces. Eso todos los agentes ya los están implementando, que es básicamente hacer que si por ejemplo dice, creas un software a service que funciona la autenticación, el cobre de usuarios y así, obviamente quizás a la primera no lo hace porque quizás termina completando algunas tareas o las deja medias. Bueno, el comando go lo que hace es que como está a medias, é mismo lo prueba y si falla otra vez vuelve a iterar e iterar hasta que cumple su objetivo. Aunque obviamente esto es básicamente lanzar como una sesión que no finaliza.

**17:52** · Ahora, en el caso de esta aplicación pues si lo revisamos ha generado esta simple interfaz que es algo bastante común de hecho. Y bueno, aquí le he dado un slash goal, entonces le he dicho, crea una sección de dashboard para administrar los usuarios de la aplicación. También debería ir con autenticación. En realidad ese es un módulo muy pequeño, pero es solamente para quitere a lo mucho un par de veces.

### Comando /goal (iteración automática)

**18:09** · Pero por ejemplo ustedes pueden darle algo mucho más genérico. Por ejemplo, crea un SAS acerca de tal tema y obviamente como le han dado un término tan genérico, pues allí obviamente no todas las tareas van a terminarse.

**18:20** · Entonces va a iterar muchas veces hasta que llegue el objetivo. Y bueno, aquí después de ciertos minutos aquí me dice, "Okay, completado, vamos a abrir la página." Y al parecer ha generado esto, aunque bueno, de momento lo ha generado con estos estilos típico de los modelos de Gemne realmente. Vamos a entrar con el usuario para ver si funciona.

**18:34** · Entonces vamos a darle admin, entramos y bueno, al parecer sí funciona la autenticación y tengo una sección admin.

**18:40** · Y bueno, al menos de momento se hace la lógica, aunque ven en cuanto a interfaz es la primer respuesta que nos da. Igual nosotros podemos cambiar de modelo, entonces aquí también podríamos cambiarlo por un 3.1 Pro o un Cloud Sonet, por ejemplo. Entonces podríamos decirle mejor la UI, pero para hacer eso mucho mejor, vamos a utilizar un skill que obviamente también Antigravity CLI lo soporta. Entonces, en esta web ustedes pueden encontrar una enorme cantidad de habilidades o aen skills para sus agentes.

### Instalar Skills (frontend-design)

**19:03** · Y como antigravity también puede leerlos desde consola, podemos instalar el que queramos, pero una recomendación es que siempre investiguen un poco de quién lo creó o qué tantos lo están utilizando, porque si simplemente instalan un skill por allí, puede que cambie algo de configuración a su sistema o simplemente puede que le estén robando información.

**19:18** · Entonces, en este caso vamos a buscar uno muy conocido que se llama Frontend Design que está creado por Antropic, es decir, la empresa que crea CloudC, pero en realidad todos estos skills se pueden instalar en una enorme cantidad de herramientas. Entonces vamos a copiar esto y voy a cancelar un segundo aquí con control D veces. Y bueno, una vez estemos dentro de la terminal, simplemente voy a navegar dentro del proyecto, es decir, dentro del proyecto que acabamos de crear en la última sesión y vamos a ejecutar el comando de skills. Es decir, lo pegamos tal cual y con esto se va a lanzar este instalador de skills. En lo personal, como pueden ver, esto lo instala dentro de una carpeta punto Entonces, incluso esto también lo lee el propio editor de antigravity.

**19:49** · Pero bueno, de momento es tan fácil como simplemente dar un enter sin seleccionar nada. Le voy a dar a nivel de proyecto sim link. Yes. Y con esto ya tenemos ahora dentro del proyecto también es skill, lo que quiere decir que si lanzo Agi y doy un enter, por ejemplo, carga G antigravity y vamos a escribir ahora el comando slash skills y doy un enter y vamos a ver que ahora tengo este skill llamado frontend design. Entonces simplemente voy a decirle algo como esto, mejora la UI de toda la app usando frontend design.

**20:11** · Y bueno, aquí un tema que tengo y que es muy importante también que lo vean es que me dice que los servidores están básicamente saturados y es porque estoy intentando utilizar cloudset, pero bueno, vamos a cambiarlo con cualquier otro modelo, por ejemplo, 3.5 flash que funcionaba bastante bien y vamos a pedirle lo mismo. Por cierto, si ustedes también quieren ejecutar sesiones anteriores, pues pueden presionar la flecha de arriba y abajo y con eso pueden navegar entre pronss anteriores que ya han pedido en el agente. Y bueno, después de unos segundos vamos a ver que aquí ya lo reescribió. Y bueno, si lo revisamos, vamos a ver qué creó este UI.

**20:39** · Vamos a generar allí, aunque hay algún uno que otro tema con un borde al parecer, pero bueno, si entramos, vamos a ver que he añadido algunas animaciones y pueden ver que no lucen nada mal, pero esto es mucho mejor de lo que ya teníamos antes. Ahora, una característica que también tiene el CLI de antigravity es este comando llamado en que como su nombre le indica, es para poder lanzar múltiples agentes y que cada gente esté enfocada en una tarea.

### Crear y usar subagentes (/agents)

**21:00** · Ahora, el tema es que si ustedes escriben slash aquí solamente les lista los que tienen instalados y de hecho solamente tienen uno que es el default y es el que típicamente nos contesta. Pero también podría decir algo como esto.

**21:10** · Crea dos agentes, uno enfocado en investigación que se llame research, y otro enfocado en testing, que se llame tester, por ejemplo. Vamos a darle ese preg y lo que vamos a ver en respuesta es definiendo subagentes. Es decir, para aquellos que no estén familiarizados con esta idea, los subagentes son básicamente un agente enfocado en una sola tarea que guardan la configuración dentro del proyecto. Por darles una idea, aquí han generado dos, uno llamado Research Specialist y otro llamado tester. Y si quieren verlo en ejecución, pueden pedir algo como esto. Haz una investigación de métodos de pago para este proyecto usando research agent.

**21:42** · Entonces, lo que se va a lanzar es el especialista que acabamos de crear. Y de esta forma nosotros podríamos estar como más confiados de que esto simplemente se va a enfocar en esa parte. De hecho, esto lo inicia y mientras va trabajando sub agente, nosotros podríamos ir haciendo cualquier otra cosa. Por ejemplo, le digo, crea los testing usando tester a y van a ver que aquí lanza aen tester y pueden ver que ahora ha lanzado otra tarea. E incluso aquí ustedes lo que van a ver es que hay dos subentes en ejecución. E incluso si ustedes escriben slash y dan un enter, van a ver que aquí justamente está lo que ya acabó uno.

**22:11** · Por ejemplo, aquí está el agente de investigación y si lo minimizamos aquí está el otro que es el agente de testing. Y podemos minimizarlos. Y bueno, de esta forma podríamos ir viéndolos allí. Ahora, aquí no me los lista como agentes disponibles por alguna razón, quizás por la configuración no lo cargó, pero aquí sí los detecta y pueden ver que justamente el enter aún está en ejecución y esto es lo que está haciendo al final, es decir, esos son los pasos que va ejecutando en su propia sesión.

**22:35** · Y de nuevo, para aquellos que no están familiarizados con los subagentes, pues básicamente es como lanzar tres terminales y cada uno va a haciendo una tarea distinta, pero en realidad todas están dentro de esta sesión. Y bueno, aquí ya terminó al parecer también el tester, es decir, concluyó el testing, el tester en y bueno, aquí podemos ver la respuesta. Y bueno, de esta forma ya tendrían un resumen de todo lo que está ofreciendo Antigravity Cli. Y bueno, este es un overview rápido, pero si veo que les interesa o al menos veo que ese tipo de herramientas llama su atención, en la siguiente también puedo darles como un miniurso acerca de todas las características que tiene, porque si bien aquí les he mencionado las principales, también tiene otras cosas bastante interesantes.

### Activar notificaciones

**23:06** · Por ejemplo, en este caso no les he hablado acerca de los MCPs, que también es una forma adicional de añadir más características.

**23:11** · Luego también incluso tiene un comando llamado schedule que es para que ustedes puedan programar tareas y obviamente también tiene hooks para poder lanzarse a medida que va terminando una tarea.

**23:19** · Por cierto, eso me recuerda que también en config ustedes tienen una sección para habilitar notificaciones, así que también les pueden dar en habilitar y esto les va a avisar cada vez que termina una respuesta, simplemente lanzando un sonido de su sistema. Por ejemplo, aquí le digo hola y allí se lanza el sonido. Okay. Y con esto ya tienen una idea de lo que hace Antigravity CLI. Si recuerdan, yo estoy utilizando el plan gratuito, así que si escribo en usage pueden ver que, okay, ahora sí ya he estado avanzando con el uso de Gemini 3.5 flash tanto en high como como en low.

### Conclusiones y opiniones finales

**23:45** · Pero bueno, aprovechan que de momento está bastante utilizable y de hecho el modelo de Gemini 3.5 funciona bastante bien y en comparación con otros agentes de IA esto responde bastante rápido. Entonces, de forma resumida sí me he presionado bastante la forma fluida que funciona este agente y a diferencia de otros agentes pagados, incluso está bastante bien. Entonces, esperemos simplemente que esto vaya avanzando, porque algo que sí me ha faltado, al menos, para este video, es poder revisar la documentación, porque de momento simplemente no hay una documentación de antigravity CLI, así que voy a esperar que la implemente en cuestión de días o quizás esta semana y ya a partir de eso quizás les traigo el curso de Antigravity CLI.

**24:15** · En fin, si tienen una duda o quisieran ver otra característica también pueden pedirlo en los comentarios. Nos vemos en un siguiente video y eso ha sido todo por el video del día de hoy. Si quieres conocer más, te dejo en pantalla mis enlaces sociales y mi web fast.dev en donde puedes reservar asesorías personalizadas de cualquier tema. Y no te olvides de dejarme un comentario, ya sea de una duda o una sugerencia para el siguiente video. Nos vemos en un próximo video.