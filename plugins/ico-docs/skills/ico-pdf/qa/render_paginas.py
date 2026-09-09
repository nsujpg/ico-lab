# -*- coding: utf-8 -*-
"""
Rasteriza el PDF final para mirarlo pagina a pagina.

Ningun script sustituye esto. Los huecos muertos, las lineas huerfanas y los
bloques desequilibrados solo se ven mirando.

Uso:
    python render_paginas.py "salida.pdf"
    python render_paginas.py "salida.pdf" --salida ./revision --escala 3
"""
import argparse
import os
import sys

try:
    import fitz  # PyMuPDF
except ImportError:
    sys.exit("Falta PyMuPDF. Instalalo con: pip install pymupdf")


def main():
    ap = argparse.ArgumentParser(description="Rasteriza un PDF para revision visual")
    ap.add_argument("pdf")
    ap.add_argument("--salida", default="./revision")
    ap.add_argument("--escala", type=float, default=2.0)
    ap.add_argument("--pagina", type=int, help="Solo esta pagina (1-indexada)")
    args = ap.parse_args()

    os.makedirs(args.salida, exist_ok=True)
    doc = fitz.open(args.pdf)
    for i, p in enumerate(doc):
        if args.pagina and i + 1 != args.pagina:
            continue
        destino = os.path.join(args.salida, "p%02d.png" % (i + 1))
        p.get_pixmap(matrix=fitz.Matrix(args.escala, args.escala)).save(destino)
        print("  %s" % destino)

    print("\nMira cada una y pregunta:")
    print("  - Hay algun hueco de mas de 30 mm que no sea margen?")
    print("  - Se lee la marca sin acercarse?")
    print("  - Se entiende cada grafica sin leer el cuerpo?")
    print("  - Hay algun bloque identico repetido mas de tres veces?")


if __name__ == "__main__":
    main()
