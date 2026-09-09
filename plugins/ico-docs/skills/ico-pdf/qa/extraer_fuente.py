# -*- coding: utf-8 -*-
"""
Saca todo lo aprovechable del PDF o del .ai que manda el cliente:

  texto.txt        el contenido integro, pagina a pagina
  paginas/*.png    cada pagina rasterizada, para mirarla
  assets/*.png     logos e imagenes, con la transparencia bien resuelta
  paleta.txt       los colores REALES, muestreados de los vectores
  tipografia.txt   fuentes y cuerpos usados

Nunca maquetes de memoria. Esto es el punto de partida de cualquier encargo.

Uso:
    python extraer_fuente.py "original.pdf"
    python extraer_fuente.py "grafico.ai" --salida ./fuente-grafico
"""
import argparse
import io
import os
import sys
from collections import Counter

try:
    import fitz  # PyMuPDF
except ImportError:
    sys.exit("Falta PyMuPDF. Instalalo con: pip install pymupdf")

try:
    from PIL import Image
except ImportError:
    sys.exit("Falta Pillow. Instalalo con: pip install pillow")


def a_hex(c):
    if c is None:
        return None
    try:
        return "#%02X%02X%02X" % tuple(int(round(v * 255)) for v in c)
    except TypeError:
        return None


def extrae_texto(doc, destino):
    with io.open(os.path.join(destino, "texto.txt"), "w", encoding="utf-8") as f:
        for i, p in enumerate(doc):
            f.write("=" * 70 + "\nPAGINA %d\n" % (i + 1) + "=" * 70 + "\n")
            f.write(p.get_text() + "\n")
    print("  texto.txt")


def rasteriza(doc, destino, escala):
    carpeta = os.path.join(destino, "paginas")
    os.makedirs(carpeta, exist_ok=True)
    for i, p in enumerate(doc):
        p.get_pixmap(matrix=fitz.Matrix(escala, escala)).save(
            os.path.join(carpeta, "p%02d.png" % (i + 1)))
    print("  paginas/  (%d)" % doc.page_count)


def extrae_assets(doc, destino):
    """Combina cada imagen con su smask; sin esto los logos salen con fondo negro."""
    carpeta = os.path.join(destino, "assets")
    os.makedirs(carpeta, exist_ok=True)
    vistos, n = set(), 0
    for pagina in doc:
        for info in pagina.get_images(full=True):
            xref = info[0]
            if xref in vistos:
                continue
            vistos.add(xref)
            try:
                d = doc.extract_image(xref)
                base = Image.open(io.BytesIO(d["image"])).convert("RGB")
                if d.get("smask"):
                    m = doc.extract_image(d["smask"])
                    mask = Image.open(io.BytesIO(m["image"])).convert("L").resize(base.size)
                    base = base.convert("RGBA")
                    base.putalpha(mask)
                base.save(os.path.join(carpeta, "img_%d.png" % xref))
                n += 1
            except Exception as e:
                print("  aviso: imagen %d no extraida (%s)" % (xref, e))
    print("  assets/   (%d)" % n)


def extrae_paleta(doc, destino):
    trazos, rellenos = Counter(), Counter()
    for pagina in doc:
        for dr in pagina.get_drawings():
            c = a_hex(dr.get("color"))
            if c:
                trazos[(c, round(dr.get("width") or 0, 1))] += 1
            f = a_hex(dr.get("fill"))
            if f:
                rellenos[f] += 1
    with io.open(os.path.join(destino, "paleta.txt"), "w", encoding="utf-8") as f:
        f.write("COLORES REALES (muestreados de los vectores, no de pixeles)\n\n")
        f.write("RELLENOS\n")
        for c, n in rellenos.most_common(30):
            f.write("  %s  x%d\n" % (c, n))
        f.write("\nTRAZOS (color, grosor)\n")
        for (c, w), n in trazos.most_common(30):
            f.write("  %s  %.1fpt  x%d\n" % (c, w, n))
    print("  paleta.txt")


def extrae_tipografia(doc, destino):
    spans = Counter()
    for pagina in doc:
        for b in pagina.get_text("dict")["blocks"]:
            if b["type"] != 0:
                continue
            for linea in b["lines"]:
                for s in linea["spans"]:
                    if s["text"].strip():
                        spans[(s["font"], round(s["size"], 1), a_hex_int(s["color"]))] += len(s["text"])
    with io.open(os.path.join(destino, "tipografia.txt"), "w", encoding="utf-8") as f:
        f.write("FUENTE, CUERPO, COLOR -> caracteres\n\n")
        for (fuente, tam, color), n in sorted(spans.items(), key=lambda x: -x[1]):
            f.write("  %-28s %6.1f pt  %s  %d\n" % (fuente, tam, color, n))
    print("  tipografia.txt")


def a_hex_int(v):
    try:
        return "#%06X" % v
    except Exception:
        return "?"


def main():
    ap = argparse.ArgumentParser(description="Extrae la fuente de verdad de un PDF o .ai")
    ap.add_argument("entrada", help="PDF o .ai del cliente")
    ap.add_argument("--salida", default="./fuente", help="Carpeta de salida")
    ap.add_argument("--escala", type=float, default=2.0, help="Escala de rasterizado")
    args = ap.parse_args()

    os.makedirs(args.salida, exist_ok=True)
    doc = fitz.open(args.entrada)
    print("\n%s -> %s" % (args.entrada, args.salida))
    print("  %d pagina(s), %.0f x %.0f mm\n"
          % (doc.page_count, doc[0].rect.width / 72 * 25.4, doc[0].rect.height / 72 * 25.4))

    extrae_texto(doc, args.salida)
    rasteriza(doc, args.salida, args.escala)
    extrae_assets(doc, args.salida)
    extrae_paleta(doc, args.salida)
    extrae_tipografia(doc, args.salida)

    print("\nSiguiente paso: mirar paginas/ antes de decidir nada.")


if __name__ == "__main__":
    main()
