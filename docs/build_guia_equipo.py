# -*- coding: utf-8 -*-
"""
Genera la guía de uso del sistema de documentos de ICO para el equipo.

Se construye con el propio sistema que documenta: misma paleta, misma
tipografía, misma retícula, mismo isotipo. Si el PDF resultante no pasa las
puertas de calidad de la skill, es que el sistema no vale.

    python build_guia_equipo.py
"""
import io
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(AQUI, "guia-equipo.html")

# ------------------------------------------------------------------ paleta
NAVY, INK, AZUL, SKY = "#172B8F", "#4D5872", "#1A52D8", "#6DB8FF"
LAV, TIP, FILETE, FILETE2 = "#EDF2FD", "#F1F5FE", "#DFE9FB", "#E5E9F2"
APAGADO, DORADO, GRAD_PLANO = "#A9B0C4", "#F1C86A", "#12297A"
GRAD = "linear-gradient(135deg,#1982DE 0%,#1242A8 30%,#12297A 62%,#0A1636 100%)"

PALETA = [
    ("#172B8F", "Navy", "Titulares, strong, bloques macizos"),
    ("#4D5872", "Tinta", "Cuerpo de texto"),
    ("#1A52D8", "Azul de acción", "Filetes, antetítulos, borde de callout"),
    ("#6DB8FF", "Azul claro", "Acentos sobre fondo oscuro"),
    ("#0068FF", "Azul del isotipo", "Solo la marca"),
    ("#EDF2FD", "Lavanda", "Paneles y callouts"),
    ("#F1F5FE", "Lavanda claro", "Caja de tip"),
    ("#DFE9FB", "Filete", "Bordes de figura y retícula"),
    ("#A9B0C4", "Apagado", "Pies y folios"),
    ("#F1C86A", "Dorado", "Subtitulares de cierre"),
]

SERIES = ["#6DB8FF", "#37B0A6", "#3F6BD6", "#F2B134"]

ESCALA = [
    ("Titular de portada", "54 pt", "playfair", 54, "Guía de productividad"),
    ("Titular de sección", "19 pt", "playfair", 19, "Ponle un límite a todo"),
    ("Cuerpo", "11,5 pt", "poppins300", 11.5,
     "Todos tenemos las mismas 24 horas. La diferencia no está en quién trabaja más."),
    ("Texto de callout", "11 pt", "poppins300", 11,
     "Elige una sola habilidad y dedícale 20 minutos cada día."),
    ("Antetítulo", "8,6 pt", "eyebrow", 8.6, "PASO 1"),
    ("Pie y folio", "8,5 pt", "poppins400", 8.5, "Instituto de Comunicación"),
]

REGLAS = [
    ("El contenido es del cliente",
     "Adaptar no es reinterpretar. Ni una palabra propia, ni resúmenes, ni cajas de "
     "consejos, ni reordenar apartados. Las erratas se reproducen tal cual y se avisan "
     "aparte, nunca se corrigen por dentro."),
    ("La marca se lee o no está",
     "Isotipo de 20 mm con el nombre al lado, en portada y cierre. Cero sellos pequeños "
     "en las esquinas de las páginas interiores: un logo que no se lee es ruido."),
    ("Cero sombras",
     "Ni en texto ni en elementos. El diseño de ICO es plano. Para legibilidad sobre foto "
     "se usa un scrim de fondo, que es tratamiento de imagen, no una sombra."),
    ("Nada por debajo de 11,5 pt",
     "En texto de lectura. Los rótulos de una figura y los folios son la única excepción, "
     "y tienen su propio suelo."),
]

FASES = [
    ("Leer la fuente de verdad",
     "Del PDF o del .ai del cliente se saca todo: el texto íntegro, las páginas en imagen, "
     "los assets con la transparencia resuelta y la paleta real muestreada de los vectores. "
     "Nunca se maqueta de memoria ni a ojo.",
     "python &lt;skill&gt;/qa/extraer_fuente.py &quot;original.pdf&quot; --salida ./fuente"),
    ("Decidir el sistema antes de maquetar",
     "Mira las páginas del original y las piezas anteriores. Decide retícula, jerarquía y "
     "ritmo, y escríbelo antes de tocar CSS. Pregunta de control: ¿esta pieza tiene un "
     "sistema, o son ocho bloques iguales repetidos?",
     None),
    ("Construir",
     "HTML y CSS impresos a PDF con un Chromium en modo headless. Los tokens del sistema "
     "están en plantilla/ico.css.",
     "&lt;chromium&gt; --headless=new --disable-gpu --no-pdf-header-footer \\\n"
     "  --print-to-pdf=&quot;salida.pdf&quot; &quot;file:///ruta/documento.html&quot;"),
    ("Pasar las puertas de calidad",
     "Se miden, no se estiman. Las dos son obligatorias antes de enseñar nada a nadie.",
     "python &lt;skill&gt;/qa/qa_maquetacion.py &quot;salida.pdf&quot; --html documento.html\n"
     "python &lt;skill&gt;/qa/qa_fidelidad.py &quot;original.pdf&quot; &quot;salida.pdf&quot;"),
    ("Mirar las páginas",
     "Un script que pasa no garantiza una página bien compuesta. Los huecos muertos, los "
     "bloques desequilibrados y las líneas huérfanas solo se ven mirando.",
     "python &lt;skill&gt;/qa/render_paginas.py &quot;salida.pdf&quot; --salida ./revision"),
]

PROBLEMAS = [
    ("El <em>marketplace add</em> no clona",
     "El repositorio es privado. Pide que te añadan como colaborador y haz "
     "<strong>gh auth login</strong> en tu máquina."),
    ("Los titulares salen con otra tipografía",
     "Faltan Poppins o Playfair Display en el sistema. Se bajan de Google Fonts y se "
     "instalan como cualquier otra fuente."),
    ("El PDF no se actualiza al reimprimir",
     "Chromium a veces termina sin escribir y sin avisar. Comprueba la fecha del archivo "
     "después de imprimir, no des por hecho que se ha escrito."),
    ("Las páginas oscuras salen en blanco en el móvil",
     "Es un degradado sin color plano debajo. Parte el atajo de CSS en "
     "<strong>background-color</strong> más <strong>background-image</strong>."),
]

ANTI_IA = [
    ("El mismo bloque repetido N veces",
     "Ocho pasos con ocho pastillas idénticas no es un sistema, es un formulario.",
     "Antetítulo más titular grande en Playfair y filete. El color estructura, no rellena."),
    ("Huecos muertos",
     "Media página en blanco al final porque el contenido se acabó. Es la firma más clara "
     "de maquetación automática.",
     "Reparte el aire, agranda la figura o recompón la paginación. Un margen inferior de "
     "20 a 25 mm es normal; 40 mm es un agujero."),
    ("Todo centrado",
     "Portada centrada, título centrado, subtítulo centrado. Seguro y anodino.",
     "Composición asimétrica, anclada abajo, con la foto a sangre."),
    ("La marca repetida en miniatura",
     "Un isotipo de 7 mm en la esquina de cada página no comunica marca.",
     "Marca grande en portada y cierre; en interiores, el nombre en el pie y nada más."),
    ("Decoración por defecto",
     "Emojis, iconos genéricos, cajas con borde alrededor de todo, subrayados de color.",
     "Un punto focal por página. Si resaltas todo, no resaltas nada: dos o tres énfasis en "
     "todo el documento."),
    ("Gráficas ilegibles",
     "Curvas sin leyenda, etiquetas flotando lejos de lo que nombran, texto girado sobre "
     "fondo de bajo contraste.",
     "Cada etiqueta pegada a su curva con un punto y una guía."),
]

OLOR = [
    "¿Hay algún bloque que aparece idéntico más de tres veces seguidas?",
    "¿Alguna página tiene más de 30 mm de blanco seguido que no sea margen?",
    "¿Se lee la marca sin acercarse?",
    "¿Cada gráfica se entiende sin leer el cuerpo del texto?",
    "¿Hay algún elemento que esté ahí solo porque quedaba hueco?",
]

PUERTAS = [
    ("qa_maquetacion.py", "Holgura al pie, cuerpos de texto, degradados y sombras", [
        "Mide en milímetros lo que hay entre el último píxel de contenido y el filete del "
        "pie. Por debajo de 3,5 mm es desborde. Caza páginas que a ojo parecen correctas.",
        "Lista los cuerpos reales y separa el texto de lectura del rótulo por volumen, "
        "media de caracteres y tipografía, para no llenar el informe de falsos avisos.",
        "Avisa de los degradados sin color plano debajo, que en muchos visores de Android "
        "dejan la página en blanco.",
        "Cuenta las sombras del HTML. Tienen que ser cero.",
    ]),
    ("qa_fidelidad.py", "Demuestra que el texto del cliente no ha cambiado", [
        "Compara la secuencia de palabras de los dos PDFs. A nivel de frase da falsos "
        "positivos por los saltos de línea; a nivel de palabra es fiable.",
        "Recompone las palabras que el letter-spacing parte en letras y clasifica como "
        "artefacto lo que tiene las mismas letras en otro troceado o las mismas palabras "
        "en otro orden.",
        "Lo que queda hay que confirmarlo mirando. Una vez comprobado se silencia con "
        "--ignorar, nunca antes.",
    ]),
]


def cod(txt):
    return '<pre class="cod">%s</pre>' % txt


def pagina(inner, folio):
    pie = ('<div class="pie"><span></span>'
           '<span class="centro">Sistema de documentos · Instituto de Comunicación</span>'
           '<span>%02d</span></div>' % folio)
    return '<div class="page"><div class="inner">%s</div>%s</div>' % (inner, pie)


def antetitulo(txt):
    return ('<div class="antetitulo"><span class="barra"></span>'
            '<span class="etiqueta">%s</span><span class="linea"></span></div>' % txt)


def seccion(eyebrow, titulo, ultima=None):
    if ultima:
        titulo = titulo.replace(ultima, "<i>%s</i>" % ultima)
    return antetitulo(eyebrow) + '<h2 class="seccion">%s</h2>' % titulo


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

h1.portada{position:absolute;left:20mm;right:22mm;top:82mm;
  font-family:'Playfair Display',Georgia,serif;font-weight:700;font-size:46pt;
  line-height:1.07;color:#fff;letter-spacing:-.7px}
h1.portada i{font-style:italic;color:__SKY__}
.portada-rule{position:absolute;left:20mm;top:186mm;width:36mm;height:2.5px;background:__SKY__}
.portada-sub{position:absolute;left:20mm;right:44mm;top:195mm;font-size:13pt;
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

.cuerpo{font-size:11.5pt;line-height:1.6;font-weight:300;color:__INK__;margin-top:3.4mm}
.cuerpo strong{font-weight:600;color:__NAVY__}
.cuerpo em{font-style:italic}

.apertura{background:__NAVY__;border-radius:6px;padding:8.5mm 9mm 8mm}
.apertura p{font-size:11.5pt;line-height:1.6;color:#D8E2F7;font-weight:300}
.apertura p+p{margin-top:3.4mm}
.apertura strong{font-weight:600;color:__SKY__}

.cod{font-family:Consolas,'Courier New',monospace;font-size:9.8pt;line-height:1.55;
  background:__TIP__;border-left:3px solid __AZUL__;border-radius:0 5px 5px 0;
  padding:3.4mm 5mm;margin-top:3.6mm;color:__NAVY__;white-space:pre-wrap;
  word-break:break-word}

.regla{display:flex;gap:5mm;margin-top:12mm}
.regla .num{font-family:'Playfair Display',Georgia,serif;font-weight:700;font-size:23pt;
  color:__AZUL__;line-height:1;flex:0 0 12mm}
.regla h3{font-family:'Playfair Display',Georgia,serif;font-weight:700;font-size:14.5pt;
  color:__NAVY__;line-height:1.2}
.regla p{font-size:11pt;line-height:1.58;font-weight:300;color:__INK__;margin-top:2mm}

.fase{margin-top:7mm}
.fase h3{font-size:12pt;font-weight:600;color:__NAVY__}
.fase h3 .n{color:__AZUL__;margin-right:2.5mm}
.fase p{font-size:11pt;line-height:1.58;font-weight:300;color:__INK__;margin-top:1.8mm}

table.paleta{width:100%;border-collapse:collapse;margin-top:5mm}
table.paleta td{padding:2.2mm 0;border-bottom:1px solid __FILETE__;vertical-align:middle}
table.paleta .chip{width:18mm}
table.paleta .chip div{width:16mm;height:9mm;border-radius:3px;
  border:1px solid rgba(0,0,0,.07)}
table.paleta .hex{font-family:Consolas,monospace;font-size:10.2pt;color:__NAVY__;
  width:27mm;font-weight:600}
table.paleta .nom{font-size:11pt;font-weight:500;color:__NAVY__;width:43mm}
table.paleta .uso{font-size:10.6pt;font-weight:300;color:__INK__}

.series{display:flex;gap:4mm;margin-top:4mm}
.series div{flex:1;text-align:center}
.series .barra{height:8mm;border-radius:3px}
.series .et{font-family:Consolas,monospace;font-size:9.2pt;color:__INK__;margin-top:1.8mm}

.tipo{border-bottom:1px solid __FILETE__;padding:4mm 0}
.tipo .meta{display:flex;gap:4mm;align-items:baseline}
.tipo .rol{font-size:8.6pt;font-weight:600;letter-spacing:1.6px;color:__AZUL__;
  text-transform:uppercase;flex:0 0 46mm}
.tipo .pt{font-family:Consolas,monospace;font-size:9.8pt;color:__NAVY__;font-weight:600}
.tipo .muestra{margin-top:2.2mm;color:__NAVY__}
.playfair{font-family:'Playfair Display',Georgia,serif;font-weight:700;line-height:1.1}
.poppins300{font-weight:300;color:__INK__;line-height:1.5}
.poppins400{font-weight:400;color:__APAGADO__}
.eyebrow{font-weight:600;letter-spacing:2.4px;color:__AZUL__;text-transform:uppercase}

.reticula{margin-top:5mm;display:flex;gap:9mm;align-items:flex-start}
.reticula .dib{flex:0 0 56mm;height:79mm;border:1px solid __NAVY__;position:relative;
  background:#fff}
.reticula .zona{position:absolute;left:4.8mm;right:4.8mm;top:4.5mm;bottom:5.2mm;
  background:__LAV__;border:1px dashed __AZUL__}
.reticula .piecito{position:absolute;left:4.8mm;right:4.8mm;bottom:2.8mm;height:1px;
  background:__APAGADO__}
.reticula ul{list-style:none;font-size:11pt;line-height:1.95;font-weight:300;color:__INK__}
.reticula li strong{font-weight:600;color:__NAVY__;font-family:Consolas,monospace;
  font-size:10.2pt}

.comp{border:1px solid __FILETE__;border-radius:7px;margin-top:4mm;overflow:hidden}
.comp .cab{background:__NAVY__;padding:2.8mm 6mm}
.comp .cab h4{font-family:'Playfair Display',Georgia,serif;font-weight:700;font-size:12pt;
  color:#fff}
.comp .interior{padding:4.4mm 6mm 5mm}
.comp .interior p{font-size:11pt;font-weight:300;line-height:1.55;color:__INK__}
.callout{background:__LAV__;border-left:3px solid __AZUL__;border-radius:0 6px 6px 0;
  padding:3.6mm 6.5mm 3.8mm 6mm}
.callout .et{font-size:8.6pt;font-weight:600;letter-spacing:2.2px;color:__AZUL__;
  text-transform:uppercase;margin-right:3.4mm}
.callout p{font-size:11pt;line-height:1.55;font-weight:300;color:__INK__;display:inline}

.mal{margin-top:4.4mm;border-left:3px solid __FILETE__;padding-left:5.5mm}
.mal h3{font-size:12pt;font-weight:600;color:__NAVY__}
.mal .que{font-size:11pt;line-height:1.55;font-weight:300;color:__INK__;margin-top:1.6mm}
.mal .en-vez{font-size:11pt;line-height:1.55;font-weight:300;color:__NAVY__;margin-top:1.6mm}
.mal .en-vez b{font-weight:600;color:__AZUL__}

.puerta{margin-top:18mm}
.puerta h3{font-family:Consolas,monospace;font-size:12.5pt;font-weight:700;color:__NAVY__}
.puerta .sub{font-size:11pt;font-weight:300;color:__INK__;margin-top:2.4mm;
  padding-bottom:4.5mm;border-bottom:1px solid __FILETE__}
.puerta ul{list-style:none;margin-top:5mm}
.puerta li{font-size:11pt;line-height:1.58;font-weight:300;color:__INK__;
  padding-left:6.5mm;position:relative;margin-top:5.4mm}
.puerta li:before{content:"";position:absolute;left:0;top:2.4mm;width:2.6mm;height:2.6mm;
  border-radius:50%;background:__AZUL__}

.olor{counter-reset:o;margin-top:8mm}
.olor li{list-style:none;font-size:11pt;line-height:1.55;font-weight:300;color:__INK__;
  padding-left:9mm;position:relative;margin-top:10mm}
.olor li:before{counter-increment:o;content:counter(o);position:absolute;left:0;top:-.4mm;
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
.cierre .codc{font-family:Consolas,monospace;font-size:10.6pt;line-height:1.62;
  color:#fff;background:rgba(255,255,255,.10);border-left:3px solid __SKY__;
  border-radius:0 5px 5px 0;padding:3.8mm 5mm;margin-top:6mm;white-space:pre-wrap}
.cierre .url{margin-top:auto;font-size:9.5pt;letter-spacing:.6px;color:#9EC2F0}
"""
for k, v in [("__NAVY__", NAVY), ("__INK__", INK), ("__AZUL__", AZUL), ("__SKY__", SKY),
             ("__LAV__", LAV), ("__TIP__", TIP), ("__FILETE__", FILETE),
             ("__FILETE2__", FILETE2), ("__APAGADO__", APAGADO), ("__DORADO__", DORADO),
             ("__GRADPLANO__", GRAD_PLANO), ("__GRAD__", GRAD)]:
    CSS = CSS.replace(k, v)

# El isotipo es el archivo real extraido de un PDF del cliente, no una reconstruccion.
MARCA = ('<div class="marca"><img src="assets/iso_white.png" alt="">'
         '<span>Instituto de<br>Comunicación</span></div>'
         '<div class="marca-filete"></div>')

# ------------------------------------------------------------------ páginas
p1 = """<div class="page oscura">
  %s
  <h1 class="portada">Sistema de documentos<br>del Instituto de <i>Comunicación</i></h1>
  <div class="portada-rule"></div>
  <p class="portada-sub">Cómo producir los PDFs del cliente sin repetir las rondas que ya
     costaron rechazos. Guía de uso para el equipo.</p>
  <div class="portada-meta"><span>Cabaña Studio</span><span>skill ico-pdf · v1.0</span></div>
</div>""" % MARCA

reglas_html = "".join(
    '<div class="regla"><div class="num">%02d</div><div><h3>%s</h3><p>%s</p></div></div>'
    % (i + 1, t, d) for i, (t, d) in enumerate(REGLAS))
p2 = pagina(
    '<div class="apertura">'
    '<p>Esto no es un manual de estilo decorativo. Es lo que hemos aprendido produciendo '
    'documentos para ICO, incluidas las veces que el cliente los devolvió: logos que no se '
    'leían, huecos muertos a media página, cuerpos de texto pequeños y ocho bloques '
    'idénticos repetidos.</p>'
    '<p>Va instalado como skill de Claude, así que no hay que recordarlo: se activa solo al '
    'pedir cualquier PDF de ICO. <strong>Lo que sí hay que conocer son las cuatro reglas de '
    'abajo</strong>, porque son las que el cliente nota.</p></div>'
    '<div style="margin-top:10mm">' + seccion("LO INNEGOCIABLE", "Cuatro reglas", "reglas")
    + reglas_html + '</div>', 2)

problemas_html = "".join(
    '<div class="mal"><h3>%s</h3><p class="que">%s</p></div>' % (t, d)
    for t, d in PROBLEMAS)
p3 = pagina(
    seccion("EMPEZAR", "Instalación en cinco minutos", "minutos")
    + '<p class="cuerpo">El repositorio es privado: pide que te añadan como colaborador '
      'antes de empezar.</p>'
    + '<div style="margin-top:5mm">' + antetitulo("1 · REQUISITOS") + '</div>'
    + '<p class="cuerpo">Python con dos librerías y las dos fuentes de la marca instaladas '
      'en el sistema: <strong>Poppins</strong> y <strong>Playfair Display</strong>, que se '
      'bajan de Google Fonts. Así el CSS no depende de la red al imprimir.</p>'
    + cod("pip install pymupdf pillow")
    + '<div style="margin-top:5mm">' + antetitulo("2 · ACCESO Y SKILL") + '</div>'
    + '<p class="cuerpo">Lo primero en la terminal, lo segundo dentro de Claude Code. '
      'Después, reinicia la sesión.</p>'
    + cod("gh auth login\n\n/plugin marketplace add nsujpg/ico-lab\n"
          "/plugin install ico-docs@ico")
    + '<p class="cuerpo">Se activa sola al pedir cualquier PDF de ICO, o a mano con '
      '<strong>/ico-docs:ico-pdf</strong>. Para actualizarla: '
      '<strong>/plugin marketplace update ico</strong>.</p>'
    + '<div style="margin-top:4mm">' + antetitulo("SI ALGO FALLA") + '</div>'
    + problemas_html, 3)

fases_html = "".join(
    '<div class="fase"><h3><span class="n">%d</span>%s</h3><p>%s</p>%s</div>'
    % (i + 1, t, d, cod(c) if c else "") for i, (t, d, c) in enumerate(FASES))
p4 = pagina(
    seccion("EL FLUJO", "Cómo se trabaja una pieza", "pieza")
    + '<p class="cuerpo">Cinco fases, siempre en el mismo orden. Las dos últimas son las que '
      'separan un documento entregable de uno que vuelve.</p>' + fases_html, 4)

paleta_html = "".join(
    '<tr><td class="chip"><div style="background:%s"></div></td><td class="hex">%s</td>'
    '<td class="nom">%s</td><td class="uso">%s</td></tr>' % (h, h, n, u)
    for h, n, u in PALETA)
series_html = "".join(
    '<div><div class="barra" style="background:%s"></div><div class="et">%s</div></div>'
    % (h, h) for h in SERIES)
p5 = pagina(
    seccion("SISTEMA VISUAL", "Color", "Color")
    + '<p class="cuerpo">Muestreados de PDFs reales aprobados por el cliente, no elegidos a '
      'ojo. Si dudas de un color, sácalo del PDF del cliente con '
      '<strong>extraer_fuente.py</strong> en vez de estimarlo.</p>'
    + '<table class="paleta">%s</table>' % paleta_html
    + '<div style="margin-top:7mm">' + antetitulo("DEGRADADO DE PORTADA Y CIERRE") + '</div>'
    + '<div style="height:14mm;border-radius:5px;margin-top:3.5mm;background-color:%s;'
      'background-image:%s"></div>' % (GRAD_PLANO, GRAD)
    + '<p class="cuerpo">Siempre con un color plano debajo. Sin él, muchos visores de PDF de '
      'Android dejan la página en blanco y el documento se pierde entero.</p>'
    + '<div style="margin-top:8mm">' + antetitulo("SERIES DE GRÁFICAS") + '</div>'
    + '<div class="series">%s</div>' % series_html, 5)

tipo_html = ""
for rol, pt, clase, tam, muestra in ESCALA:
    est = "font-size:%gpt" % tam
    if clase == "eyebrow":
        est += ";letter-spacing:2.4px"
    tipo_html += ('<div class="tipo"><div class="meta"><span class="rol">%s</span>'
                  '<span class="pt">%s</span></div><div class="muestra %s" style="%s">%s'
                  '</div></div>' % (rol, pt, clase, est, muestra))
p6 = pagina(
    seccion("SISTEMA VISUAL", "Tipografía", "Tipografía")
    + '<p class="cuerpo"><strong>Playfair Display 700 solo en titulares</strong>, nunca en '
      'cuerpo, etiquetas ni pastillas, y nunca en mayúsculas. <strong>Poppins para todo lo '
      'demás</strong>: Light 300 en cuerpo, 500 y 600 en etiquetas.</p>'
    + '<div style="margin-top:5mm">%s</div>' % tipo_html
    + '<div style="margin-top:8mm">' + antetitulo("EL PATRÓN FIRMADO") + '</div>'
    + '<p class="cuerpo">La última palabra del titular va en itálica y en azul. Sobre fondo '
      'oscuro, en azul claro.</p>'
    + '<h2 class="seccion" style="margin-top:4mm">Diseña tu día para entrar en <i>flow</i></h2>'
    + '<p class="cuerpo">Ojo con las tildes en titulares grandes: comprueba que no invadan '
      'la línea de arriba.</p>', 6)

p7 = pagina(
    seccion("SISTEMA VISUAL", "Retícula y componentes", "componentes")
    + '<div class="reticula"><div class="dib"><div class="zona"></div>'
      '<div class="piecito"></div></div><ul>'
      '<li>Página <strong>210 × 297 mm</strong></li>'
      '<li>Márgenes <strong>18 mm</strong> laterales</li>'
      '<li>Superior <strong>17 mm</strong></li>'
      '<li>Inferior <strong>19,5 mm</strong></li>'
      '<li>Columna de texto <strong>174 mm</strong></li>'
      '<li>Filete del pie a <strong>10,5 mm</strong></li>'
      '<li>Holgura mínima <strong>3,5 mm</strong></li></ul></div>'
    + '<p class="cuerpo">La holgura al pie se mide con el script, no a ojo: una caja puede '
      'quedar a 1 mm del filete y parecer correcta en pantalla.</p>'
    + '<div style="margin-top:8mm">' + antetitulo("ANTETÍTULO DE SECCIÓN") + '</div>'
    + '<div style="margin-top:4mm">' + antetitulo("PASO 1")
    + '<h2 class="seccion">La mentalidad del <i>1%</i></h2></div>'
    + '<div style="margin-top:8mm">' + antetitulo("CALLOUT") + '</div>'
    + '<div class="callout" style="margin-top:4mm"><span class="et">Tip práctico</span>'
      '<p>Sin emoji y sin icono decorativo. La etiqueta en versalitas azules, en línea con '
      'el texto.</p></div>'
    + '<div style="margin-top:8mm">' + antetitulo("FIGURA") + '</div>'
    + '<div class="comp"><div class="cab"><h4>Título de la figura</h4></div>'
      '<div class="interior"><p>Banda navy arriba solo si la figura tenía título en el '
      'original. Si el cliente ya la ha dibujado, se usa su vector: sale mejor que cualquier '
      'reconstrucción y respeta su trabajo.</p></div></div>', 7)

anti_html = "".join(
    '<div class="mal"><h3>%s</h3><p class="que">%s</p>'
    '<p class="en-vez"><b>En su lugar:</b> %s</p></div>' % (t, q, e)
    for t, q, e in ANTI_IA)
p8 = pagina(
    seccion("LO QUE SE NOTA", "Lo que delata a una máquina", "máquina")
    + '<p class="cuerpo">Un PDF puede cumplir la paleta, la tipografía y la retícula y aun '
      'así cantar. Esto es lo que lo canta.</p>' + anti_html, 8)

puertas_html = ""
for nombre, sub, puntos in PUERTAS:
    lis = "".join("<li>%s</li>" % p for p in puntos)
    puertas_html += ('<div class="puerta"><h3>%s</h3><div class="sub">%s</div><ul>%s</ul>'
                     '</div>' % (nombre, sub, lis))
olor_html = "".join("<li>%s</li>" % o for o in OLOR)
p9 = pagina(
    seccion("ANTES DE ENTREGAR", "Las puertas de calidad", "calidad")
    + '<p class="cuerpo">Se miden. <strong>"Se ve bien" no es una puerta.</strong> Las dos se '
      'pasan siempre antes de enseñar el documento a nadie, y al entregar se dice qué se '
      'midió.</p>' + puertas_html, 9)

p10 = pagina(
    seccion("ANTES DE ENTREGAR", "Y después, los <i>ojos</i>")
    + '<p class="cuerpo">Renderiza las páginas y míralas una a una. Ningún script detecta un '
      'hueco muerto, un bloque desequilibrado, una línea huérfana ni un titular que parte '
      'mal.</p>'
    + cod("python &lt;skill&gt;/qa/render_paginas.py &quot;salida.pdf&quot; --salida ./revision")
    + '<div style="margin-top:12mm">' + antetitulo("LA PRUEBA DE OLOR") + '</div>'
    + '<p class="cuerpo">Con las páginas delante, cinco preguntas:</p>'
    + '<ol class="olor">%s</ol>' % olor_html
    + '<p class="cuerpo" style="margin-top:7mm">Un sí en la primera, la segunda o la quinta, '
      'o un no en la tercera o la cuarta, es una ronda más antes de enseñarlo.</p>'
    + '<div style="margin-top:12mm">' + antetitulo("Y AL ENTREGAR") + '</div>'
    + '<p class="cuerpo">Di qué has medido. <strong>"Holgura al pie de 7,9 a 24,9 mm, '
      'fidelidad sin diferencias reales, cero sombras"</strong> vale más que "quedó bien". '
      'Y si has encontrado una errata o una incoherencia en el material del cliente, se '
      'señala en el mensaje, nunca se corrige por dentro.</p>', 10)

p11 = """<div class="page oscura">
  %s
  <div class="cierre">
    <h2>Si algo de esto se queda corto, se cambia en el repositorio.</h2>
    <h3>Dónde está todo</h3>
    <p>La skill vive en <strong>nsujpg/ico-lab</strong>. Las referencias completas están
       dentro, en <strong>references/</strong>: marca, anti-ia, fidelidad, qa, gráficas y
       toolchain. Se leen igual de bien sin Claude delante.</p>
    <p>Los valores de la paleta y la tipografía están muestreados de PDFs reales aprobados.
       Si el cliente cambia algo, se vuelve a muestrear con el script, no se estima.</p>
    <div class="codc">/plugin marketplace add nsujpg/ico-lab
/plugin install ico-docs@ico</div>
    <div class="url">Cabaña Studio · humbertocabana.com</div>
  </div>
</div>""" % MARCA

html = ('<!doctype html><html lang="es"><head><meta charset="utf-8">'
        '<title>Sistema de documentos ICO</title><style>%s</style></head><body>'
        '%s%s%s%s%s%s%s%s%s%s%s</body></html>'
        % (CSS, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11))

io.open(SALIDA, "w", encoding="utf-8").write(html)
print("OK -> %s  (%d bytes)" % (SALIDA, len(html)))
