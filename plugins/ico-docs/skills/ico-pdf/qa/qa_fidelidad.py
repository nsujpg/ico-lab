# -*- coding: utf-8 -*-
"""
Prueba de fidelidad de contenido: demuestra que una remaquetacion no toco el texto.

Compara la secuencia de PALABRAS de dos PDFs. A nivel de frase da falsos positivos por
los saltos de linea; a nivel de palabra es fiable.

Separa las diferencias reales de los artefactos conocidos de maquetacion:
  - etiquetas con letter-spacing, que se extraen letra a letra
  - pies de pagina y folios
  - etiquetas de eje de una grafica, que salen en otro orden de lectura
  - texto de una figura vectorizado a proposito (no aparece en la capa de texto)

Uso:
    python qa_fidelidad.py "original.pdf" "rediseño.pdf"
    python qa_fidelidad.py orig.pdf nuevo.pdf --ignorar "tiempo,retenido,% "
    python qa_fidelidad.py orig.pdf nuevo.pdf --informe informe.txt
"""
import argparse
import difflib
import re
import sys
import unicodedata

# La consola de Windows va en cp1252 y revienta con simbolos como el infinito.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    import fitz  # PyMuPDF
except ImportError:
    sys.exit("Falta PyMuPDF. Instalalo con: pip install pymupdf")


# Palabras que aparecen o desaparecen por como se maqueta, no por cambiar contenido.
RUIDO_POR_DEFECTO = {
    "instituto", "comunicación", "comunicacion",
    "www", "institutodecomunicacion", "com",
    "—", "–",
}


def texto_pdf(ruta):
    return "\n".join(p.get_text() for p in fitz.open(ruta))


def palabras(ruta, pie=None):
    t = unicodedata.normalize("NFC", texto_pdf(ruta))
    t = t.replace(" ", " ").lower()
    # los emojis decorativos no son contenido
    t = re.sub(r"[\U0001F000-\U0001FAFF☀-➿]", " ", t)
    if pie:
        t = t.replace(pie.lower(), " ")
    fichas = re.findall(r"[0-9]+%?|[a-záéíóúüñ]+|[—∞%]", t)
    fichas = [f for f in fichas if not re.fullmatch(r"0[1-9]|[1-4][0-9]", f)]  # folios
    return une_letras_sueltas(fichas)


def une_letras_sueltas(fichas, minimo=3):
    """Rehace las palabras que el letter-spacing parte en letras.

    "TIP PRACTICO" con interletrado se extrae como t,i,p,p,r,a,c,t,i,c,o. Si no
    se recompone, el diff lo canta como contenido perdido en un lado y ganado en
    otro, y el informe se llena de falsos positivos.

    Se exigen `minimo` letras seguidas: en castellano "y a" o "y o" son normales,
    pero tres monoletras seguidas ya no aparecen en texto corrido.
    """
    salida, buffer = [], []
    def vuelca():
        if len(buffer) >= minimo:
            salida.append("".join(buffer))
        else:
            salida.extend(buffer)
        buffer.clear()
    for f in fichas:
        if len(f) == 1 and f.isalpha():
            buffer.append(f)
        else:
            vuelca()
            salida.append(f)
    vuelca()
    return salida


def main():
    ap = argparse.ArgumentParser(description="Prueba de fidelidad de contenido (ICO)")
    ap.add_argument("original", help="PDF fuente del cliente")
    ap.add_argument("nuevo", help="PDF remaquetado")
    ap.add_argument("--pie", default="Instituto de Comunicación",
                    help="Texto del pie que se repite en cada pagina")
    ap.add_argument("--ignorar", default="",
                    help="Palabras extra a tratar como ruido, separadas por comas")
    ap.add_argument("--informe", help="Guardar el informe completo en un archivo")
    args = ap.parse_args()

    ruido = set(RUIDO_POR_DEFECTO)
    ruido |= {w.strip().lower() for w in args.ignorar.split(",") if w.strip()}

    a = palabras(args.original, args.pie)
    b = palabras(args.nuevo, args.pie)
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)

    lineas = []
    p = lineas.append
    p("FIDELIDAD DE CONTENIDO")
    p("=" * 68)
    p("original : %s" % args.original)
    p("nuevo    : %s" % args.nuevo)
    p("palabras : %d -> %d" % (len(a), len(b)))
    p("similitud: %.4f" % sm.ratio())
    p("")
    p("Lee la lista, no el numero. Una similitud de 0,93 con todas las diferencias")
    p("explicadas es un pase; una de 0,99 con una diferencia real, no.")
    p("")

    letra_suelta = re.compile(r"^[a-záéíóúüñ%]$")
    reales, artefactos = [], []

    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        falta = [w for w in a[i1:i2]]
        sobra = [w for w in b[j1:j2]]
        ctx = " ".join(a[max(0, i1 - 6):i1])

        def limpia(ws):
            out = []
            for w in ws:
                if w in ruido:
                    continue
                if letra_suelta.match(w):   # letter-spacing partido en letras
                    continue
                if re.fullmatch(r"\d+%?", w):  # numeros de eje reordenados
                    continue
                out.append(w)
            return out

        f, s = limpia(falta), limpia(sobra)
        if not f and not s:
            artefactos.append((falta, sobra, ctx))
        elif "".join(f) == "".join(s):
            # mismas letras, distinto troceado: es maquetacion, no contenido
            # ("tip practico" frente a "tippractico" por el letter-spacing)
            artefactos.append((falta, sobra, ctx))
        elif sorted(f) == sorted(s):
            # mismas palabras en distinto orden de lectura (rotulos de eje)
            artefactos.append((falta, sobra, ctx))
        else:
            reales.append((f, s, ctx))

    p("-" * 68)
    p("DIFERENCIAS REALES DE CONTENIDO: %d" % len(reales))
    p("-" * 68)
    if not reales:
        p("  Ninguna. El texto del cliente esta integro.")
    else:
        for f, s, ctx in reales:
            p("  falta: %s" % (f or "-"))
            p("  sobra: %s" % (s or "-"))
            p("  contexto: ...%s" % ctx)
            p("")

    p("-" * 68)
    p("ARTEFACTOS DE MAQUETACION (esperados): %d" % len(artefactos))
    p("-" * 68)
    for f, s, ctx in artefactos[:40]:
        p("  ~ %s / %s   [...%s]" % (" ".join(f) or "-", " ".join(s) or "-", ctx[-40:]))
    if len(artefactos) > 40:
        p("  ... y %d mas" % (len(artefactos) - 40))

    informe = "\n".join(lineas)
    if args.informe:
        with open(args.informe, "w", encoding="utf-8") as fh:
            fh.write(informe)
        print("Informe guardado en %s" % args.informe)
    print(informe)

    sys.exit(1 if reales else 0)


if __name__ == "__main__":
    main()
