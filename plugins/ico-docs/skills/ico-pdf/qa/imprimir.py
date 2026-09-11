# -*- coding: utf-8 -*-
"""
Imprime un HTML a PDF en A4.

Usa el Chromium que trae Playwright en vez del navegador del sistema. Llamar a
Edge o a Chrome por linea de comandos funciona hasta que deja de funcionar:
se engancha a una instancia ya abierta, sale con codigo 0 y no escribe nada,
y te deja trabajando sobre un PDF viejo sin enterarte. Playwright arranca su
propio navegador aislado y falla de forma ruidosa.

    python imprimir.py documento.html salida.pdf

Si falta el navegador:  python -m playwright install chromium
"""
import argparse
import os
import sys

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("Falta Playwright. Instalalo con:\n"
             "    pip install playwright\n"
             "    python -m playwright install chromium")


def imprimir(html, pdf, espera=400):
    html = os.path.abspath(html)
    pdf = os.path.abspath(pdf)
    if not os.path.exists(html):
        sys.exit("No existe el HTML: %s" % html)

    antes = os.path.getmtime(pdf) if os.path.exists(pdf) else None

    with sync_playwright() as p:
        navegador = p.chromium.launch()
        pagina = navegador.new_page()
        pagina.goto("file:///" + html.replace(os.sep, "/"), wait_until="networkidle")
        pagina.wait_for_timeout(espera)
        pagina.pdf(path=pdf, format="A4", print_background=True,
                   prefer_css_page_size=True,
                   margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
        navegador.close()

    # Comprobar que de verdad se ha escrito, no fiarse del codigo de salida.
    if not os.path.exists(pdf):
        sys.exit("El navegador termino pero no escribio el PDF.")
    despues = os.path.getmtime(pdf)
    if antes is not None and despues <= antes:
        sys.exit("El PDF no se ha actualizado. Estarias revisando una version vieja.")

    print("%s  (%.0f KB)" % (pdf, os.path.getsize(pdf) / 1024))
    return pdf


def main():
    ap = argparse.ArgumentParser(description="HTML a PDF en A4 (ICO)")
    ap.add_argument("html")
    ap.add_argument("pdf")
    ap.add_argument("--espera", type=int, default=400,
                    help="Milisegundos extra tras cargar, para fuentes y SVG")
    args = ap.parse_args()
    imprimir(args.html, args.pdf, args.espera)


if __name__ == "__main__":
    main()
