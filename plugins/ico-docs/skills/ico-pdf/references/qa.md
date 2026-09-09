# Puertas de calidad

Se miden. "Se ve bien" no es una puerta.

## 1. Maquetación — `qa/qa_maquetacion.py`

**Holgura al pie.** Localiza el filete del pie (fila gris con blanco puro justo encima) y
mide en milímetros hasta el último píxel de contenido. Por debajo de **3,5 mm** es
desborde. Cazó tres páginas que a ojo parecían correctas: la caja de callout terminaba a
1 mm del filete.

**Textos pequeños.** Recorre los `span` del PDF y lista los cuerpos reales. Cualquier texto
de lectura por debajo de 11,5 pt es un fallo. Los subíndices y los folios son la excepción
legítima; el script los señala para que los mires, no los aprueba solo.

**Degradados sin respaldo plano.** Ver `toolchain.md`. Busca `scn` en el content stream y
avisa de las páginas que quedarían en blanco en un visor que no pinte patrones.

**Sombras.** `grep` sobre el HTML: `text-shadow|drop-shadow|box-shadow` debe dar 0.

## 2. Fidelidad — `qa/qa_fidelidad.py`

Ver `fidelidad.md`.

## 3. Los ojos

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
