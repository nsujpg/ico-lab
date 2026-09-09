# -*- coding: utf-8 -*-
"""
Puerta de calidad de maquetacion para PDFs de ICO.

Comprueba cuatro cosas que a ojo no se ven:
  1. Holgura entre el ultimo pixel de contenido y el filete del pie (en mm).
  2. Cuerpos de texto reales, para cazar cualquier cosa por debajo del minimo.
  3. Degradados sin color plano debajo (se pierden en visores PDF de Android).
  4. Sombras en el HTML de origen, si se pasa con --html.

Uso:
    python qa_maquetacion.py "salida.pdf"
    python qa_maquetacion.py "salida.pdf" --html documento.html --min-holgura 3.5

Salida: informe por consola y codigo de salida 1 si algo falla, para poder
encadenarlo en un script de build.
"""
import argparse
import re
import sys
from collections import Counter

# La consola de Windows va en cp1252 y revienta con simbolos como "inf" o acentos.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    import fitz  # PyMuPDF
except ImportError:
    sys.exit("Falta PyMuPDF. Instalalo con: pip install pymupdf")

try:
    from PIL import Image
except ImportError:
    sys.exit("Falta Pillow. Instalalo con: pip install pillow")


ESCALA = 4.0  # px por punto al rasterizar

a_px = lambda mm: mm / 25.4 * 72 * ESCALA
a_mm = lambda px: px / ESCALA / 72 * 25.4


def pagina_a_imagen(pagina):
    pm = pagina.get_pixmap(matrix=fitz.Matrix(ESCALA, ESCALA))
    return Image.frombytes("RGB", (pm.width, pm.height), pm.samples)


def busca_filete_pie(im, x0, x1):
    """El filete del pie es una fila gris clara con blanco puro justo encima."""
    for y in range(int(a_px(292)), int(a_px(266)), -1):
        if y >= im.height:
            continue
        gris = sum(1 for x in range(x0, x1, 4)
                   if 4 < 255 - min(im.getpixel((x, y))) < 60)
        if gris < (x1 - x0) / 4 * 0.9:
            continue
        blanco = sum(1 for x in range(x0, x1, 4)
                     if min(im.getpixel((x, y - 5))) > 250)
        if blanco > (x1 - x0) / 4 * 0.97:
            return y
    return None


def ultimo_pixel_contenido(im, x0, x1, desde_y):
    """Primer pixel con tinta subiendo desde `desde_y`. Salta el antialias del filete."""
    for y in range(desde_y - int(a_px(1.2)), int(a_px(120)), -1):
        if any(255 - min(im.getpixel((x, y))) > 10 for x in range(x0, x1, 2)):
            return y
    return None


def revisa_holguras(doc, margen_lateral, min_holgura):
    print("=" * 68)
    print("1. HOLGURA AL PIE  (minimo %.1f mm)" % min_holgura)
    print("=" * 68)
    fallos = 0
    for i, pagina in enumerate(doc):
        im = pagina_a_imagen(pagina)
        x0 = int(a_px(margen_lateral))
        x1 = int(a_px(210 - margen_lateral))
        filete = busca_filete_pie(im, x0, x1)
        if filete is None:
            print("   p%-2d  sin filete de pie (portada, cierre o pagina a sangre)" % (i + 1))
            continue
        ultimo = ultimo_pixel_contenido(im, x0, x1, filete)
        if ultimo is None:
            print("   p%-2d  filete en %.1f mm, sin contenido por encima" % (i + 1, a_mm(filete)))
            continue
        holgura = a_mm(filete - ultimo)
        ok = holgura >= min_holgura
        fallos += 0 if ok else 1
        print("   p%-2d  filete %.1f mm | contenido acaba %.1f mm | holgura %5.1f mm  %s"
              % (i + 1, a_mm(filete), a_mm(ultimo), holgura,
                 "OK" if ok else "<-- DESBORDE"))
    return fallos


def revisa_cuerpos(doc, min_lectura, min_absoluto, umbral_corrido=300):
    """Distingue texto corrido de etiqueta suelta por volumen de caracteres.

    Un cuerpo de 11 pt con 1.400 caracteres es el texto de los callouts y esta
    bien. Un cuerpo de 10 pt con 19 caracteres es el rotulo de un eje. Aplicar
    el mismo umbral a los dos llena el informe de ruido y ensena a ignorarlo.
    """
    print("=" * 68)
    print("2. CUERPOS DE TEXTO  (texto corrido >= %.1f pt | absoluto >= %.1f pt)"
          % (min_lectura, min_absoluto))
    print("=" * 68)
    tam = Counter()
    ejemplos = {}
    for i, pagina in enumerate(doc):
        for b in pagina.get_text("dict")["blocks"]:
            if b["type"] != 0:
                continue
            for linea in b["lines"]:
                for span in linea["spans"]:
                    txt = span["text"].strip()
                    if not txt:
                        continue
                    k = round(span["size"], 1)
                    tam[k] += len(txt)
                    ejemplos.setdefault(k, (i + 1, txt[:38]))
    fallos = 0
    for k in sorted(tam, reverse=True):
        n = tam[k]
        corrido = n >= umbral_corrido
        malo = (corrido and k < min_lectura) or (k < min_absoluto)
        pag, muestra = ejemplos[k]
        etiqueta = "corrido" if corrido else "rotulo "
        aviso = "  <-- FALLO (p%d: %r)" % (pag, muestra) if malo else ""
        if malo:
            fallos += 1
        print("   %5.1f pt  %s %5d car.%s" % (k, etiqueta, n, aviso))
    if not fallos:
        print()
        print("   Sin fallos. Los cuerpos pequenos son rotulos, subindices y folios.")
    return fallos


def revisa_degradados(doc):
    print("=" * 68)
    print("3. DEGRADADOS SIN COLOR PLANO DEBAJO")
    print("=" * 68)
    afectadas = []
    for i, pagina in enumerate(doc):
        try:
            contenido = pagina.read_contents()
        except Exception:
            continue
        if re.search(rb"/P\d+ (scn|SCN)", contenido):
            afectadas.append(i + 1)
    if not afectadas:
        print("   Ninguna pagina usa patrones de sombreado.")
        return 0
    print("   Paginas con degradado: %s" % ", ".join("p%d" % p for p in afectadas))
    print()
    print("   Comprueba que cada una tenga un color plano debajo. Si no, en muchos")
    print("   visores de Android el area queda en blanco y la pagina se pierde.")
    print("   CSS: background-color:#plano; background-image:linear-gradient(...)")
    return 0  # aviso, no fallo automatico


def revisa_sombras(ruta_html):
    print("=" * 68)
    print("4. SOMBRAS EN EL HTML")
    print("=" * 68)
    if not ruta_html:
        print("   (sin --html, omitido)")
        return 0
    try:
        with open(ruta_html, encoding="utf-8") as f:
            html = f.read()
    except OSError as e:
        print("   No se puede leer el HTML: %s" % e)
        return 0
    hits = re.findall(r"text-shadow|drop-shadow|box-shadow", html)
    if hits:
        print("   %d sombras encontradas: %s" % (len(hits), Counter(hits)))
        print("   El diseno de ICO es plano. Quitalas todas.")
        return 1
    print("   Cero sombras. OK")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Puerta de calidad de maquetacion (ICO)")
    ap.add_argument("pdf", help="PDF a revisar")
    ap.add_argument("--html", help="HTML de origen, para buscar sombras")
    ap.add_argument("--margen-lateral", type=float, default=18.0,
                    help="Margen lateral de la reticula en mm (por defecto 18)")
    ap.add_argument("--min-holgura", type=float, default=3.5,
                    help="Holgura minima al filete del pie en mm (por defecto 3,5)")
    ap.add_argument("--min-lectura", type=float, default=11.0,
                    help="Cuerpo minimo del texto corrido en pt (por defecto 11)")
    ap.add_argument("--min-absoluto", type=float, default=7.5,
                    help="Suelo para cualquier texto en pt (por defecto 7,5)")
    args = ap.parse_args()

    doc = fitz.open(args.pdf)
    print()
    print("PDF: %s" % args.pdf)
    print("     %d paginas, %.0f x %.0f mm"
          % (doc.page_count, doc[0].rect.width / 72 * 25.4, doc[0].rect.height / 72 * 25.4))
    print()

    fallos = 0
    fallos += revisa_holguras(doc, args.margen_lateral, args.min_holgura)
    fallos += revisa_cuerpos(doc, args.min_lectura, args.min_absoluto)
    revisa_degradados(doc)
    fallos += revisa_sombras(args.html)

    print("=" * 68)
    if fallos:
        print("RESULTADO: %d fallo(s). No entregar hasta corregirlos." % fallos)
        sys.exit(1)
    print("RESULTADO: sin fallos automaticos.")
    print("Falta lo que ningun script ve: mira las paginas renderizadas una a una.")


if __name__ == "__main__":
    main()
