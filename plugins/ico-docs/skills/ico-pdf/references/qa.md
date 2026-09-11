# Puertas de calidad

Se miden. "Se ve bien" no es una puerta.

## 1. Maquetación — `qa/qa_maquetacion.py`

**Holgura al pie.** Localiza el filete del pie (fila gris con blanco puro justo encima) y
mide en milímetros hasta el último píxel de contenido. Por debajo de **3,5 mm** es
desborde. Cazó tres páginas que a ojo parecían correctas: la caja de callout terminaba a
1 mm del filete.

**Textos pequeños.** Separa el texto de lectura del rótulo antes de aplicar el mínimo, con
tres señales medidas sobre PDFs reales: volumen total, media de caracteres por span
(lectura 40-52, etiquetas y pies 21-25) y tipografía (lo monoespaciado es código, nunca
lectura). Sin la media, un antetítulo repetido 27 veces suma 630 caracteres y se cuela como
párrafo: el informe se llena de ruido y la gente aprende a ignorarlo.

**Degradados sin respaldo plano.** Ver `toolchain.md`. Busca `scn` en el content stream y
avisa de las páginas que quedarían en blanco en un visor que no pinte patrones.

**Sombras.** `grep` sobre el HTML: `text-shadow|drop-shadow|box-shadow` debe dar 0.

## 2. Fidelidad — `qa/qa_fidelidad.py`

Ver `fidelidad.md`.

## 3. Imprimir — `qa/imprimir.py`

```bash
python qa/imprimir.py documento.html salida.pdf
```

Chromium propio y verificación de que el archivo se ha actualizado. Un código de salida 0
no significa que se haya escrito el PDF.

## 4. Los ojos

Renderiza las páginas y míralas una a una:

```bash
python qa/render_paginas.py "salida.pdf" --salida ./revision
```

Lo que ningún script detecta:

- Huecos muertos y bloques desequilibrados.
- Líneas viudas y huérfanas.
- Una figura que técnicamente cabe pero aplasta la página.
- Un titular que parte mal.
- La sensación general de "esto lo ha hecho una máquina".

## Orden

Maquetación y fidelidad primero, porque son baratas y objetivas. Los ojos al final, sobre
un PDF que ya pasa las dos.

Y antes de entregar: di qué has medido. "Holgura al pie 7,9–24,9 mm, fidelidad sin
diferencias reales, cero sombras" vale más que "quedó bien".
