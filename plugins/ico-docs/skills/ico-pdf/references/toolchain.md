# Entorno y trampas conocidas

## Lo que hace falta

```bash
pip install pymupdf pillow
```

**Un Chromium para imprimir el HTML a PDF.** Cualquiera vale; se usa el que haya:

| Sistema | Ruta habitual |
|---|---|
| Windows | `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe` |
| Windows | `C:\Program Files\Google\Chrome\Application\chrome.exe` |
| macOS | `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome` |
| macOS | `/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge` |

**Poppins y Playfair Display instaladas en el sistema.** Se bajan de Google Fonts y se
instalan como fuentes normales. Con eso basta `font-family:'Poppins'` en el CSS, sin
`@font-face` ni enlaces externos, y la impresión no depende de la red.

**PyMuPDF para todo lo demás.** Rasterizar páginas, extraer texto, sacar assets y muestrear
color. Si tu entorno no tiene poppler, la herramienta de lectura de PDFs de Claude falla;
PyMuPDF cubre el hueco.

## HTML a PDF

```bash
<chromium> --headless=new --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="salida.pdf" "file:///ruta/con%20espacios/documento.html"
```

Respeta `@page{size:A4;margin:0}` y `print-color-adjust:exact`.

## Trampas

**Los degradados no son píxeles.** Salen como patrones de sombreado (`/Pattern cs /Pn scn`).
Muchos visores PDF de Android de serie no los pintan: el área queda en blanco y solo se
dibuja el eje del degradado como una raya diagonal. Con texto claro encima, la página se
pierde entera.

Regla: **todo degradado lleva un color plano debajo.**

```css
/* mal: el shorthand pone background-color en transparent */
background: linear-gradient(135deg, #1982DE, #0A1636);

/* bien */
background-color: #12297A;
background-image: linear-gradient(135deg, #1982DE, #0A1636);
```

En SVG, duplicar el elemento: uno con `fill="#plano"` y encima el mismo con `fill="url(#grad)"`.

Para auditarlo, buscar `scn` en `page.read_contents()`. Caza las páginas afectadas aunque
el HTML no lo delate, porque los degradados dentro de un SVG no aparecen al buscar
`linear-gradient`. Es lo que hace `qa_maquetacion.py`.

**Los enlaces salen subrayados.** `text-decoration:none` en los botones.

**Los logos extraídos salen con fondo negro.** `doc.extract_image(xref)` devuelve la imagen
base sin el canal alfa; hay que combinarla con su `smask` a mano:

```python
d = doc.extract_image(xref)
base = Image.open(io.BytesIO(d["image"])).convert("RGB")
if d.get("smask"):
    m = doc.extract_image(d["smask"])
    mask = Image.open(io.BytesIO(m["image"])).convert("L").resize(base.size)
    base = base.convert("RGBA"); base.putalpha(mask)
```

`extraer_fuente.py` ya lo hace.

**El `letter-spacing` rompe la capa de texto.** "TÚ PUEDES" con interletrado se extrae como
"T Ú  P U E D E S". Visualmente perfecto, pero un diff ingenuo lo canta como contenido
perdido. `qa_fidelidad.py` recompone esas palabras antes de comparar.

**Muestrear color.** `page.get_drawings()` da los `color` y `fill` vectoriales reales.
Sacar el color de un píxel del render da valores contaminados por el antialias.

**Consolas en cp1252 (Windows).** `print` revienta con "∞" y con acentos. Los scripts de
`qa/` ya fuerzan UTF-8 en la salida; si escribes uno nuevo, haz lo mismo:

```python
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
```

**PowerShell 5.1 y UTF-8.** `-replace` corrompe los acentos al editar archivos. Usa `sed`,
heredocs de Bash o las herramientas de edición.
