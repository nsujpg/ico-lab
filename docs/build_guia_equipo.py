# -*- coding: utf-8 -*-
"""
Genera la guía de uso del sistema de documentos de ICO.

Va dirigida a personas NO tecnicas: cada paso dice donde entrar, que descargar
y que escribir, literalmente. Nadie tiene que saber que es pip ni abrir una
terminal; lo que haga falta instalar se lo pide a Claude.

Se construye con el propio sistema que documenta. Si el PDF no pasa las puertas
de calidad de la skill, es que el sistema no vale.

    python build_guia_equipo.py
"""
import io
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(AQUI, "guia-equipo.html")

NAVY, INK, AZUL, SKY = "#172B8F", "#4D5872", "#1A52D8", "#6DB8FF"
LAV, TIP, FILETE, FILETE2 = "#EDF2FD", "#F1F5FE", "#DFE9FB", "#E5E9F2"
APAGADO, DORADO, GRAD_PLANO = "#A9B0C4", "#F1C86A", "#12297A"
GRAD = "linear-gradient(135deg,#1982DE 0%,#1242A8 30%,#12297A 62%,#0A1636 100%)"

MAC = "https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect"
WIN = "https://claude.ai/api/desktop/win32/x64/setup/latest/redirect"
GIT = "https://git-scm.com/downloads/win"
PLANES = "https://claude.com/pricing"
POPPINS = "https://fonts.google.com/specimen/Poppins"
PLAYFAIR = "https://fonts.google.com/specimen/Playfair+Display"
REPO = "https://github.com/nsujpg/ico-lab"

PALETA = [
    ("#172B8F", "Navy", "Titulares y bloques macizos"),
    ("#4D5872", "Tinta", "Cuerpo de texto"),
    ("#1A52D8", "Azul de acción", "Filetes, antetítulos y callouts"),
    ("#6DB8FF", "Azul claro", "Acentos sobre fondo oscuro"),
    ("#EDF2FD", "Lavanda", "Paneles y cajas de tip"),
    ("#F1C86A", "Dorado", "Subtitulares de cierre"),
]

REGLAS = [
    ("El contenido es del cliente",
     "Si estás adaptando algo que ICO ya ha escrito, el texto va íntegro. Ni una palabra "
     "propia, ni resúmenes, ni cajas de consejos, ni reordenar apartados. Si ves una "
     "errata, no la corrijas: avísala aparte."),
    ("La marca se lee o no está",
     "El isotipo va a 20 mm con el nombre al lado, en portada y cierre. Nada de sellos "
     "pequeños en las esquinas de las páginas interiores: un logo que no se lee es ruido."),
    ("Cero sombras",
     "El diseño de ICO es plano. Ni sombras en el texto ni en las cajas."),
    ("Nada por debajo de 11,5 pt",
     "En todo el texto que se lee. Solo los rótulos de una gráfica y los números de página "
     "pueden ir más pequeños."),
]

ANTI_IA = [
    ("El mismo bloque repetido una y otra vez",
     "Ocho apartados con ocho cajas idénticas no es un diseño, es un formulario."),
    ("Huecos muertos",
     "Media página en blanco al final porque el texto se acabó. Es lo que más canta."),
    ("Todo centrado",
     "Portada centrada, título centrado, subtítulo centrado. Seguro y anodino."),
    ("La marca repetida en miniatura",
     "Un logo de 7 mm en la esquina de cada página no comunica marca."),
    ("Decoración por defecto",
     "Emojis, iconos genéricos y cajas con borde alrededor de todo."),
    ("Gráficas que no se entienden",
     "Etiquetas flotando lejos de la línea que nombran, o texto girado sobre fondo oscuro."),
]

OLOR = [
    "¿Hay algún bloque idéntico repetido más de tres veces seguidas?",
    "¿Alguna página tiene más de un tercio en blanco?",
    "¿Se lee la marca sin acercar la nariz a la pantalla?",
    "¿Se entiende cada gráfica sin leer el texto de alrededor?",
    "¿Hay algo puesto solo porque quedaba hueco?",
]

PROBLEMAS = [
    ("La pestaña Code me pide pasar a un plan de pago",
     "Claude Code no entra en el plan gratuito. Necesitas Pro, Max, Team o Enterprise."),
    ("Escribo /plugin y no aparece nada",
     "Estás en la pestaña Chat. Los comandos de barra solo funcionan en <strong>Code</strong>."),
    ("Instalé el sistema y Claude sigue sin conocerlo",
     "Cierra Claude y vuelve a abrirlo. Compruébalo escribiendo <strong>/plugin list</strong>."),
    ("Los titulares salen con una tipografía rara",
     "Faltan Poppins o Playfair Display. Vuelve al paso 3 e instálalas."),
    ("Claude dice que le falta un programa o una librería",
     "Pídele que lo instale él: <em>«instala lo que te falte y vuelve a intentarlo»</em>."),
    ("En Windows no me deja elegir carpeta",
     "Falta Git. Instálalo desde git-scm.com/downloads/win y reinicia Claude."),
]


def cod(txt):
    return '<pre class="cod">%s</pre>' % txt


def enlace(url, texto=None):
    return '<a class="link" href="%s">%s</a>' % (url, texto or url)


def decir(texto):
    return ('<div class="decir"><span class="et">Escríbele esto</span><p>%s</p></div>'
            % texto)


def pagina(inner, folio):
    pie = ('<div class="pie"><span></span>'
           '<span class="centro">Sistema de documentos · Instituto de Comunicación</span>'
           '<span>%02d</span></div>' % folio)
    return '<div class="page"><div class="inner">%s</div>%s</div>' % (inner, pie)


def antetitulo(txt):
    return ('<div class="antetitulo"><span class="barra"></span>'
            '<span class="etiqueta">%s</span><span class="linea"></span></div>' % txt)


def paso(n, titulo, intro, bloques):
    h = ('<div class="cab-paso"><div class="np">%d</div>'
         '<div><div class="et-paso">PASO %d</div>'
         '<h2 class="tp">%s</h2></div></div>' % (n, n, titulo))
    if intro:
        h += '<p class="cuerpo">%s</p>' % intro
    return h + "".join(bloques)


def listo(texto):
    return ('<div class="listo"><span class="et">Sabrás que ha ido bien cuando</span>'
            '<p>%s</p></div>' % texto)


def sub(texto, extra=""):
    return ('<div class="sub"><div class="punto"></div><div><p>%s</p>%s</div></div>'
            % (texto, extra))


CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-family:'Poppins','Segoe UI',sans-serif;color:__INK__;background:#fff}
@page{size:A4;margin:0}
.page{width:210mm;height:297mm;position:relative;overflow:hidden;background:#fff;
  page-break-after:always;break-after:page}
.page:last-child{page-break-after:auto;break-after:auto}
.inner{position:absolute;left:18mm;right:18mm;top:17mm;bottom:19.5mm}

.oscura{background-color:__GRADPLANO__;background-image:__GRAD__}
.marca{position:absolute;top:24mm;left:20mm;display:flex;align-items:center;gap:7mm}
.marca img{width:20mm;height:20mm;display:block}
.marca span{font-family:'Playfair Display',Georgia,serif;font-weight:700;font-size:16pt;
  line-height:1.2;color:#fff;letter-spacing:.2px}
.marca-filete{position:absolute;left:20mm;right:20mm;top:58mm;height:1px;
  background:rgba(255,255,255,.3)}

h1.portada{position:absolute;left:20mm;right:26mm;top:84mm;
  font-family:'Playfair Display',Georgia,serif;font-weight:700;font-size:42pt;
  line-height:1.08;color:#fff;letter-spacing:-.6px}
h1.portada i{font-style:italic;color:__SKY__}
.portada-rule{position:absolute;left:20mm;top:196mm;width:36mm;height:2.5px;background:__SKY__}
.portada-sub{position:absolute;left:20mm;right:40mm;top:205mm;font-size:13pt;
  line-height:1.55;color:#CFE0FF;font-weight:300}
.portada-meta{position:absolute;left:20mm;right:20mm;bottom:22mm;
  border-top:1px solid rgba(255,255,255,.22);padding-top:6mm;
  display:flex;justify-content:space-between;font-size:9.5pt;color:#9EC2F0;
  letter-spacing:.6px}

.antetitulo{display:flex;align-items:center;gap:3.6mm}
.antetitulo .barra{width:9mm;height:2.6px;background:__AZUL__;flex:0 0 auto}
.antetitulo .etiqueta{font-size:8.6pt;font-weight:600;letter-spacing:2.4px;
  color:__AZUL__;text-transform:uppercase}
.antetitulo .linea{flex:1;height:1.4px;background:__NAVY__;opacity:.22}
h2.seccion{font-family:'Playfair Display',Georgia,serif;font-weight:700;font-size:20pt;
  line-height:1.14;color:__NAVY__;letter-spacing:-.2px;margin-top:1.8mm}
h2.seccion i{font-style:italic;color:__AZUL__}

.cab-paso{display:flex;gap:6mm;align-items:center}
.cab-paso .np{font-family:'Playfair Display',Georgia,serif;font-weight:700;font-size:40pt;
  color:__AZUL__;line-height:.9;flex:0 0 18mm}
.cab-paso .et-paso{font-size:8.6pt;font-weight:600;letter-spacing:2.4px;color:__AZUL__}
.cab-paso .tp{font-family:'Playfair Display',Georgia,serif;font-weight:700;font-size:21pt;
  line-height:1.14;color:__NAVY__;margin-top:1.4mm}

.cuerpo{font-size:12.5pt;line-height:1.65;font-weight:300;color:__INK__;margin-top:5.5mm}
.cuerpo strong{font-weight:600;color:__NAVY__}
.cuerpo em{font-style:italic}
.link{color:__AZUL__;font-weight:500;text-decoration:none;word-break:break-all}

.sub{display:flex;gap:5mm;margin-top:9mm}
.sub .punto{flex:0 0 3.4mm;height:3.4mm;border-radius:50%;background:__AZUL__;margin-top:2.6mm}
.sub p{font-size:12.5pt;line-height:1.65;font-weight:300;color:__INK__}
.sub p strong{font-weight:600;color:__NAVY__}
.sub p em{font-style:italic}

.apertura{background:__NAVY__;border-radius:6px;padding:8mm 9mm 7.6mm}
.apertura p{font-size:12.5pt;line-height:1.65;color:#D8E2F7;font-weight:300}
.apertura p+p{margin-top:3.4mm}
.apertura strong{font-weight:600;color:__SKY__}

.cod{font-family:Consolas,'Courier New',monospace;font-size:11.5pt;line-height:1.75;
  background:__TIP__;border-left:3px solid __AZUL__;border-radius:0 5px 5px 0;
  padding:4.4mm 5.5mm;margin-top:4.2mm;color:__NAVY__;white-space:pre-wrap;
  word-break:break-word}
.decir{background:__LAV__;border-left:3px solid __AZUL__;border-radius:0 6px 6px 0;
  padding:5mm 6.5mm 5.2mm;margin-top:4.2mm}
.decir .et{font-size:8.6pt;font-weight:600;letter-spacing:2.2px;color:__AZUL__;
  text-transform:uppercase;display:block;margin-bottom:2.2mm}
.decir p{font-size:12.5pt;line-height:1.65;font-weight:300;color:__NAVY__;font-style:italic}

.listo{border:1.6px solid __AZUL__;border-radius:6px;padding:5mm 6.5mm 5.4mm;
  margin-top:9mm}
.listo .et{font-size:8.6pt;font-weight:600;letter-spacing:2.2px;color:__AZUL__;
  text-transform:uppercase;display:block;margin-bottom:2.4mm}
.listo p{font-size:12.5pt;line-height:1.65;font-weight:300;color:__NAVY__}
.listo p strong{font-weight:600}

.checklist{margin-top:4mm}
.checklist li{list-style:none;font-size:12.5pt;line-height:1.65;font-weight:300;
  color:__INK__;padding-left:8.5mm;position:relative;margin-top:7.5mm}
.checklist li:before{content:"";position:absolute;left:0;top:1.8mm;width:4mm;height:4mm;
  border:1.6px solid __AZUL__;border-radius:2px}
.checklist li strong{font-weight:600;color:__NAVY__}

table.paleta{width:100%;border-collapse:collapse;margin-top:4mm}
table.paleta td{padding:4.2mm 0;border-bottom:1px solid __FILETE__;vertical-align:middle}
table.paleta .chip{width:18mm}
table.paleta .chip div{width:16mm;height:9mm;border-radius:3px;
  border:1px solid rgba(0,0,0,.07)}
table.paleta .hex{font-family:Consolas,monospace;font-size:10.2pt;color:__NAVY__;
  width:27mm;font-weight:600}
table.paleta .nom{font-size:12pt;font-weight:500;color:__NAVY__;width:43mm}
table.paleta .uso{font-size:11.5pt;font-weight:300;color:__INK__}

.tipo{border-bottom:1px solid __FILETE__;padding:6mm 0}
.tipo .rol{font-size:8.6pt;font-weight:600;letter-spacing:1.6px;color:__AZUL__;
  text-transform:uppercase}
.tipo .muestra{margin-top:2.4mm;color:__NAVY__}
.playfair{font-family:'Playfair Display',Georgia,serif;font-weight:700;line-height:1.1}
.poppins300{font-weight:300;color:__INK__;line-height:1.5}

.mal{margin-top:12mm;border-left:3px solid __FILETE__;padding-left:5.5mm}
.mal h3{font-size:14pt;font-weight:600;color:__NAVY__}
.mal .que{font-size:12.5pt;line-height:1.65;font-weight:300;color:__INK__;margin-top:1.6mm}

.olor{counter-reset:o;margin-top:7mm}
.olor li{list-style:none;font-size:13pt;line-height:1.65;font-weight:300;color:__INK__;
  padding-left:10.5mm;position:relative;margin-top:11.5mm}
.olor li:before{counter-increment:o;content:counter(o);position:absolute;left:0;top:-.6mm;
  font-family:'Playfair Display',Georgia,serif;font-weight:700;font-size:13pt;color:__AZUL__}

.pie{position:absolute;left:18mm;right:18mm;bottom:10.5mm;border-top:1px solid __FILETE2__;
  padding-top:2.8mm;display:flex;justify-content:space-between;align-items:center;
  font-size:8.5pt;color:__APAGADO__;letter-spacing:.3px}
.pie .centro{position:absolute;left:0;right:0;text-align:center}

.cierre{position:absolute;left:20mm;right:20mm;top:76mm;bottom:20mm;
  display:flex;flex-direction:column}
.cierre h2{font-family:'Playfair Display',Georgia,serif;font-weight:700;font-size:27pt;
  line-height:1.14;color:#fff;letter-spacing:-.4px}
.cierre h3{font-family:'Playfair Display',Georgia,serif;font-weight:700;font-size:17.5pt;
  color:__DORADO__;margin-top:11mm}
.cierre p{font-size:11.5pt;line-height:1.62;color:#D5E4FA;font-weight:300;margin-top:4.4mm}
.cierre p strong{font-weight:600;color:#fff}
.cierre .link{color:__SKY__}
.cierre .url{margin-top:auto;font-size:9.5pt;letter-spacing:.6px;color:#9EC2F0}
"""
for k, v in [("__NAVY__", NAVY), ("__INK__", INK), ("__AZUL__", AZUL), ("__SKY__", SKY),
             ("__LAV__", LAV), ("__TIP__", TIP), ("__FILETE__", FILETE),
             ("__FILETE2__", FILETE2), ("__APAGADO__", APAGADO), ("__DORADO__", DORADO),
             ("__GRADPLANO__", GRAD_PLANO), ("__GRAD__", GRAD)]:
    CSS = CSS.replace(k, v)

MARCA = ('<div class="marca"><img src="assets/iso_white.png" alt="">'
         '<span>Instituto de<br>Comunicación</span></div>'
         '<div class="marca-filete"></div>')

# ------------------------------------------------------------------- páginas
p1 = """<div class="page oscura">
  %s
  <h1 class="portada">Cómo diseñar los documentos del Instituto de <i>Comunicación</i></h1>
  <div class="portada-rule"></div>
  <p class="portada-sub">El sistema visual de la marca, cómo se monta una pieza y qué
     comprobar antes de enviarla.</p>
  <div class="portada-meta"><span>Cabaña Studio</span><span>skill ico-pdf · v1.0</span></div>
</div>""" % MARCA

p2 = pagina(
    '<div class="apertura">'
    '<p>Una guía para diseñar los documentos del Instituto de Comunicación: guías, lead '
    'magnets, dosieres y one-pagers. Recoge el sistema visual de la marca, cómo se monta '
    'una pieza de principio a fin y las comprobaciones que pasa antes de salir.</p>'
    '<p>Los tres primeros pasos se hacen <strong>una sola vez</strong>. Del cuarto en '
    'adelante es lo que harás cada vez que necesites un documento.</p>'
    '</div>'
    + '<div style="margin-top:12mm">' + antetitulo("EN ESTE DOCUMENTO ENCONTRARÁS") + '</div>'
    + '<ul class="checklist">'
      '<li><strong>Cómo dejarlo todo listo</strong> — pasos 1 a 4, una sola vez.</li>'
      '<li><strong>Cómo pedir un documento</strong> y cómo darle indicaciones — paso 5.</li>'
      '<li><strong>Qué comprobar antes de enviarlo</strong> — paso 6.</li>'
      '<li><strong>Las reglas de la marca</strong> y cómo reconocer un documento mal '
      'resuelto.</li>'
      '<li><strong>Qué hacer si algo falla.</strong></li>'
      '</ul>'
    + '<div style="margin-top:12mm">' + antetitulo("ANTES DE EMPEZAR") + '</div>'
    + '<ul class="checklist">'
      '<li>Un plan de pago de Claude: <strong>Pro, Max, Team o Enterprise</strong>. El '
      'gratuito no sirve. Los planes están en ' + enlace(PLANES) + '</li>'
      '<li>Un ordenador con <strong>Windows o Mac</strong> y conexión a internet.</li>'
      '<li><strong>Veinte minutos</strong> la primera vez.</li>'
      '</ul>', 2)

p3 = pagina(
    paso(1, "Instalar Claude en tu ordenador",
         "Se descarga, se instala y se abre. Cinco minutos.",
         [sub("Descarga el instalador que corresponda a tu ordenador.<br>"
              "<strong>Mac:</strong> " + enlace(MAC, "claude.ai/api/desktop/darwin/…") +
              "<br><strong>Windows:</strong> " + enlace(WIN, "claude.ai/api/desktop/win32/…")),
          sub("Ábrelo y sigue los pasos de instalación. Cuando acabe, abre "
              "<strong>Claude</strong> desde el menú de inicio en Windows o desde "
              "Aplicaciones en Mac."),
          sub("Inicia sesión con tu cuenta."),
          sub("Arriba en el centro verás tres pestañas: <strong>Chat</strong>, "
              "<strong>Cowork</strong> y <strong>Code</strong>. Pulsa "
              "<strong>Code</strong>: es la única que vas a usar. Si al pulsarla te pide "
              "pasar a un plan de pago, es que tu cuenta todavía no lo incluye."),
          sub("<strong>Solo en Windows:</strong> necesitas tener Git instalado o Claude no "
              "te dejará elegir una carpeta. Se descarga de " + enlace(GIT) + " y se "
              "instala dejando todas las opciones como vienen."),
          listo("Se abre la pestaña <strong>Code</strong> sin pedirte nada y te deja "
                "elegir una carpeta de tu ordenador.")]), 3)

p4 = pagina(
    paso(2, "Instalar el sistema de ICO",
         "Esto es lo que le enseña a Claude la marca, las reglas y las comprobaciones. "
         "Se hace una sola vez.",
         [sub("En la pestaña <strong>Code</strong>, elige <strong>Local</strong> y pulsa "
              "<strong>Select folder</strong>. Escoge la carpeta donde vayas a guardar los "
              "documentos de ICO. Si no tienes ninguna, crea una en el escritorio y "
              "selecciónala."),
          sub("En el recuadro donde se escribe, escribe esto y pulsa Enter:",
              cod("/plugin marketplace add nsujpg/ico-lab")),
          sub("Cuando termine, escribe esto y pulsa Enter:",
              cod("/plugin install ico-docs@ico")),
          sub("<strong>Cierra Claude y vuelve a abrirlo.</strong> Si no lo reinicias, "
              "parecerá que no se ha instalado."),
          sub("Para comprobar que está, escribe <strong>/plugin list</strong>.")]
         + [listo("En la lista aparece <strong>ico-docs</strong>. Con eso, Claude ya "
                  "conoce la marca de ICO y todas sus reglas.")]), 4)

p5 = pagina(
    paso(3, "Instalar las dos tipografías",
         "Son las de la marca. Sin ellas los títulos salen con otra letra y el documento no "
         "parece de ICO.",
         [sub("Entra en " + enlace(POPPINS) + " y pulsa <strong>Get font</strong> y luego "
              "<strong>Download all</strong>."),
          sub("Haz lo mismo en " + enlace(PLAYFAIR) + "."),
          sub("Se te habrán descargado dos archivos comprimidos. Ábrelos y descomprímelos."),
          sub("<strong>En Windows:</strong> entra en la carpeta, selecciona todos los "
              "archivos acabados en <strong>.ttf</strong>, haz clic derecho y elige "
              "<strong>Instalar</strong>.<br><strong>En Mac:</strong> selecciona todos los "
              "<strong>.ttf</strong>, haz doble clic y pulsa <strong>Instalar fuente</strong>."),
          sub("No hace falta reiniciar nada."),
          listo("Al escribir «Poppins» en el buscador de fuentes de tu ordenador, o en "
                "el desplegable de letras de Word, aparece en la lista. Y lo mismo con "
                "«Playfair Display».")]), 5)

p6 = pagina(
    paso(4, "Dejar que Claude prepare el resto",
         "Faltan un par de herramientas de fondo. Se piden y se instalan solas.",
         [sub("Abre Claude en la pestaña <strong>Code</strong> y escríbele esto tal cual:",
              decir("Vamos a hacer documentos del Instituto de Comunicación con la skill "
                    "ico-pdf. Comprueba si tengo instalado todo lo que necesita y, si falta "
                    "algo, instálalo tú y dime cuando esté listo.")),
          sub("Claude te irá pidiendo permiso para ejecutar cosas. Dile que sí. La primera "
              "vez tarda un par de minutos."),
          sub("Cuando te diga que está listo, ya no tendrás que volver a hacer esto nunca "
              "más en este ordenador."),
          listo("Claude te confirma que tiene todo lo que necesita. Si te dice que le "
                "falta algo y no puede instalarlo, pégale el mensaje de error tal cual "
                "y déjale intentarlo otra vez.")]), 6)

p7 = pagina(
    paso(5, "Pedirle el documento",
         "Cuanto más concreto seas, menos vueltas dará. Estos son los dos casos que te "
         "vas a encontrar.",
         [sub("<strong>Si estás rediseñando algo que ya existe</strong>, guarda el archivo "
              "del cliente en la carpeta que elegiste y dile:",
              decir("En la carpeta tienes «guia-productividad.pdf», que me ha pasado el "
                    "cliente. Rediséñalo con el sistema de ICO. El texto tiene que quedar "
                    "igual, palabra por palabra.")),
          sub("<strong>Si es un documento nuevo</strong>, dale el texto y explícale de qué va:",
              decir("Móntame una guía de ICO de seis páginas con este texto. Es un lead "
                    "magnet, así que la portada tiene que entrar por los ojos y la última "
                    "página lleva el botón a la masterclass.")),
          sub("Si algo no te convence, díselo con normalidad: <em>«la portada está sosa»</em>, "
              "<em>«la página 4 tiene un hueco enorme abajo»</em>, <em>«el logo se ve "
              "pequeño»</em>. Rehacerlo le cuesta segundos."),
          listo("Tienes un PDF en la carpeta y Claude te ha enseñado las páginas. "
                "Todavía no lo des por bueno: falta el paso 6.")]), 7)

p8 = pagina(
    paso(6, "Comprobarlo antes de darlo por bueno",
         "El sistema trae dos comprobaciones automáticas. El resultado hay que exigirlo: "
         "si no lo ves, no está comprobado.",
         [sub("Antes de aceptar nada, pídele esto:",
              decir("Pásale las dos puertas de calidad y enséñame los números. Y ábreme "
                    "las páginas para verlas.")),
          sub("<strong>La primera comprobación</strong> mide si algún texto se sale por "
              "abajo, si hay letra demasiado pequeña y si las páginas oscuras se verían en "
              "blanco en un móvil. Tiene que decir <strong>sin fallos</strong>."),
          sub("<strong>La segunda</strong> solo aplica cuando adaptas algo del cliente: "
              "compara palabra por palabra y demuestra que el texto no se ha tocado. Tiene "
              "que decir <strong>ninguna diferencia real</strong>."),
          sub("Y después míralo tú. Ningún programa detecta que una página esté fea: para "
              "eso tienes las cinco preguntas de la página 11."),
          listo("Claude te ha dado <strong>números concretos</strong> y las páginas "
                "abiertas para mirarlas. Si te contesta «quedó bien» sin enseñarte "
                "nada, no está comprobado: vuelve a pedírselo.")]), 8)

reglas_html = "".join(
    '<div class="mal"><h3>%d. %s</h3><p class="que">%s</p></div>' % (i + 1, t, d)
    for i, (t, d) in enumerate(REGLAS))
p9 = pagina(
    antetitulo("LO INNEGOCIABLE")
    + '<h2 class="seccion">Cuatro <i>reglas</i></h2>'
    + '<p class="cuerpo">Son las que se notan cuando fallan, y las que hacen que un '
      'documento vuelva del cliente.</p>'
    + reglas_html, 9)

anti_html = "".join(
    '<div class="mal"><h3>%s</h3><p class="que">%s</p></div>' % (t, d) for t, d in ANTI_IA)
p10 = pagina(
    antetitulo("CÓMO SABER SI ESTÁ BIEN")
    + '<h2 class="seccion">Lo que delata a una <i>máquina</i></h2>'
    + '<p class="cuerpo">Un documento puede cumplir los colores y la tipografía y aun así '
      'parecer hecho en cadena. Esto es lo que lo delata.</p>'
    + anti_html, 10)

olor_html = "".join("<li>%s</li>" % o for o in OLOR)
p11 = pagina(
    antetitulo("CÓMO SABER SI ESTÁ BIEN")
    + '<h2 class="seccion">Cinco preguntas antes de <i>enviarlo</i></h2>'
    + '<p class="cuerpo">Con las páginas delante, hazte estas cinco preguntas. Si respondes '
      'que sí a la 1, la 2 o la 5, o que no a la 3 o la 4, pídele otra vuelta.</p>'
    + '<ol class="olor">%s</ol>' % olor_html
    + '<div style="margin-top:13mm">' + antetitulo("Y UNA COSA MÁS") + '</div>'
    + '<p class="cuerpo">Si encuentras una errata en el material que te ha pasado el '
      'cliente, <strong>no la corrijas dentro del documento</strong>. Avísasela por mensaje. '
      'El texto es suyo, y arreglarlo por tu cuenta es lo que convierte una adaptación en '
      'otra cosa.</p>', 11)

paleta_html = "".join(
    '<tr><td class="chip"><div style="background:%s"></div></td><td class="hex">%s</td>'
    '<td class="nom">%s</td><td class="uso">%s</td></tr>' % (h, h, n, u)
    for h, n, u in PALETA)
p12 = pagina(
    antetitulo("PARA QUE LO RECONOZCAS")
    + '<h2 class="seccion">Los colores y las <i>letras</i></h2>'
    + '<p class="cuerpo">Están aquí para que reconozcas de un vistazo cuándo algo se ha '
      'salido de la marca.</p>'
    + '<table class="paleta">%s</table>' % paleta_html
    + '<div style="margin-top:10mm">' + antetitulo("LAS DOS TIPOGRAFÍAS") + '</div>'
    + '<div class="tipo"><div class="rol">Playfair Display · solo en titulares</div>'
      '<div class="muestra playfair" style="font-size:22pt">Ponle un límite a todo</div></div>'
    + '<div class="tipo"><div class="rol">Poppins · todo lo demás</div>'
      '<div class="muestra poppins300" style="font-size:11.5pt">Todos tenemos las mismas 24 '
      'horas. La diferencia no está en quién trabaja más, sino en quién sabe cómo funciona su '
      'propio cerebro.</div></div>'
    + '<p class="cuerpo">Los titulares nunca van en mayúsculas, y la última palabra va en '
      'cursiva y en azul. Es el detalle que hace que un documento se reconozca como de ICO.</p>',
    12)

problemas_html = "".join(
    '<div class="mal"><h3>%s</h3><p class="que">%s</p></div>' % (t, d) for t, d in PROBLEMAS)
p13 = pagina(
    antetitulo("SI ALGO FALLA")
    + '<h2 class="seccion">Los tropiezos más <i>comunes</i></h2>'
    + problemas_html
    + '<p class="cuerpo" style="margin-top:10mm">Cualquier otra cosa, <strong>cuéntala tal '
      'cual</strong> y pega el mensaje de error si lo hay. Casi todo se resuelve en el '
      'momento.</p>', 13)

p14 = """<div class="page oscura">
  %s
  <div class="cierre">
    <h2>El sistema está para usarlo, y para cambiarlo cuando haga falta.</h2>
    <h3>Si algo se te queda corto</h3>
    <p>El sistema completo vive en <strong>%s</strong>. Ahí están todas las referencias: la
       marca, las gráficas, las comprobaciones y el detalle técnico, por si alguna vez hace
       falta mirarlo.</p>
    <p>Si ves que falta algo o que una regla ya no encaja, dilo. Esto se cambia, y el cambio
       le llega a todo el equipo escribiendo
       <strong>/plugin marketplace update ico</strong>.</p>
    <div class="url">Cabaña Studio · humbertocabana.com</div>
  </div>
</div>""" % (MARCA, enlace(REPO, "github.com/nsujpg/ico-lab"))

html = ('<!doctype html><html lang="es"><head><meta charset="utf-8">'
        '<title>Cómo hacer un documento de ICO</title><style>%s</style></head><body>'
        '%s%s%s%s%s%s%s%s%s%s%s%s%s%s</body></html>'
        % (CSS, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14))

io.open(SALIDA, "w", encoding="utf-8").write(html)
print("OK -> %s  (%d bytes)" % (SALIDA, len(html)))
