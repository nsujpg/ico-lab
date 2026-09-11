---
name: ico-pdf
description: Usar al crear, rediseñar, maquetar o revisar cualquier PDF del Instituto de Comunicación (ICO) — guías, lead magnets, dosieres, informes, one-pagers. Se activa también con "guía de ICO", "lead magnet de Adrià", "maquétame este PDF", "rediseña este PDF", "el PDF del cliente queda mediocre", "revisa este PDF antes de enviarlo". Cubre el sistema visual, la regla de fidelidad de contenido y las puertas de calidad medidas.
metadata:
  version: 1.0.0
---

# PDFs del Instituto de Comunicación

Sistema para producir PDFs de ICO que no parezcan hechos por una máquina.

El material de ICO lo revisa Adrià, que es exigente con la composición y ha rechazado
piezas por cosas concretas: logos que no se leen, huecos muertos, cuerpos pequeños,
bloques repetidos. Este documento recoge lo que ha costado esas rondas.

## Las cuatro reglas que no se negocian

1. **El contenido es del cliente.** Adaptar no es reinterpretar. Ni una palabra propia,
   ni resúmenes, ni cajas de consejos, ni reordenar apartados. Las erratas se reproducen
   tal cual y se avisan aparte. Ver `references/fidelidad.md`.
2. **La marca se lee o no está.** Isotipo de 20 mm con el nombre al lado en portada y
   cierre. Cero sellos pequeños en las esquinas de las páginas interiores.
3. **Cero sombras.** Ni en texto ni en elementos. El diseño de ICO es plano.
4. **Nada por debajo de 11,5 pt** en texto de lectura.

## El proceso

### 1. Leer la fuente de verdad

Los scripts de `qa/` viven en la carpeta de esta skill. Invócalos con su ruta completa:
la que acabas de usar para leer este SKILL.md, no una ruta relativa al proyecto.

Nunca maquetes de memoria ni a ojo. Del PDF o del `.ai` del cliente se saca todo:

```bash
python <skill>/qa/extraer_fuente.py "ruta/al/original.pdf" --salida ./fuente
```

Devuelve el texto íntegro, las páginas en PNG, los assets con transparencia y la paleta
real muestreada de los vectores. Los colores se sacan de `page.get_drawings()`, no de un
píxel del render.

Si el cliente ha dibujado una gráfica en Illustrator, **úsala**: el `.ai` se abre como PDF
y se extrae a SVG vectorial. Sale mejor que cualquier reconstrucción. Ver `references/graficas.md`.

### 2. Decidir el sistema antes de maquetar

Mira las páginas renderizadas del original y las piezas anteriores de ICO. Decide la
retícula, la jerarquía y el ritmo. Escríbelo antes de tocar CSS.

Pregunta de control: ¿esta pieza tiene un sistema, o son ocho bloques iguales repetidos?
Si es lo segundo, todavía no hay diseño. Ver `references/anti-ia.md`.

### 3. Construir

HTML + CSS impreso a PDF. Los tokens del sistema visual están en
`plantilla/ico.css`; la retícula y los componentes, en `references/marca.md`.

```bash
python <skill>/qa/imprimir.py documento.html salida.pdf
```

Usa el Chromium de Playwright y **comprueba que el archivo se ha escrito de verdad**.
Llamar a Edge o Chrome por línea de comandos funciona hasta que deja de funcionar: se
engancha a una instancia abierta, sale con código 0 y no escribe nada, y te deja
revisando un PDF viejo sin enterarte.

Detalles del entorno que ahorran horas en `references/toolchain.md`.

### 4. Puertas de calidad

Se miden, no se estiman. Las dos son obligatorias antes de enseñar nada:

```bash
python <skill>/qa/qa_maquetacion.py "salida.pdf" --html documento.html
python <skill>/qa/qa_fidelidad.py "original.pdf" "salida.pdf"
```

`qa_fidelidad.py` deja fuera solo los artefactos que puede demostrar (mismas letras en
otro troceado, mismas palabras en otro orden). Lo que quede hay que confirmarlo mirando;
una vez comprobado, se silencia con `--ignorar "palabra1,palabra2"`.

`qa_maquetacion.py` ha cazado desbordes en páginas que a ojo parecían correctas, y
degradados sin respaldo plano que dejan la página en blanco en móviles Android.

### 5. Mirar las páginas

Renderiza cada página a PNG y míralas. Un script que pasa no garantiza una página bien
compuesta: los huecos muertos, los bloques desequilibrados y las líneas huérfanas solo se
ven mirando.

```bash
python <skill>/qa/render_paginas.py "salida.pdf" --salida ./revision
```

## Al entregar

Di qué has medido y qué has cambiado. Si has encontrado una errata o una incoherencia en
el material del cliente, se señala en el mensaje, nunca se corrige por dentro.

## Referencias

| Archivo | Para qué |
|---|---|
| `references/marca.md` | Colores, tipografía, retícula, componentes |
| `references/anti-ia.md` | Lo que delata a una máquina, en diseño y en texto |
| `references/fidelidad.md` | Regla de contenido íntegro y cómo demostrarla |
| `references/qa.md` | Las puertas de calidad y sus umbrales |
| `references/graficas.md` | Gráficas: reusar el vector del cliente o rehacerlas legibles |
| `references/toolchain.md` | Entorno, comandos y trampas conocidas |
