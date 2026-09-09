# ico-lab

Marketplace de Claude Code con las herramientas de trabajo del **Instituto de Comunicación**.

## Instalar

Dos comandos dentro de Claude Code, una sola vez:

```
/plugin marketplace add humberto-ui/ico-lab
/plugin install ico-docs@ico
```

Reinicia la sesión y listo. A partir de ahí la skill se activa sola cuando pidas cualquier
PDF de ICO, o a mano con `/ico-docs:ico-pdf`.

Para actualizar cuando se publiquen cambios:

```
/plugin marketplace update ico
```

## Qué instala

### `ico-docs` → skill `ico-pdf`

Sistema para producir documentos de ICO que no parezcan hechos por una máquina. Recoge lo
aprendido en las piezas anteriores, incluidas las rondas que costaron rechazos: logos que
no se leían, huecos muertos, cuerpos pequeños, bloques repetidos.

**Las cuatro reglas que no se negocian**

1. El contenido es del cliente. Adaptar no es reinterpretar. Las erratas se reproducen y
   se avisan aparte.
2. La marca se lee o no está. Cero sellos pequeños en las esquinas.
3. Cero sombras. El diseño de ICO es plano.
4. Nada por debajo de 11,5 pt en texto de lectura.

**Lo que trae**

| | |
|---|---|
| `SKILL.md` | El flujo en cinco fases |
| `references/marca.md` | Colores, tipografía, retícula, componentes |
| `references/anti-ia.md` | Lo que delata a una máquina, en diseño y en texto |
| `references/fidelidad.md` | Regla de contenido íntegro y cómo demostrarla |
| `references/qa.md` | Las puertas de calidad y sus umbrales |
| `references/graficas.md` | Reusar el vector del cliente o rehacer la gráfica legible |
| `references/toolchain.md` | Entorno, comandos y trampas conocidas |
| `plantilla/ico.css` | Los tokens del sistema visual |
| `qa/` | Cuatro scripts de comprobación |

**Los scripts**

- `extraer_fuente.py` — saca del PDF del cliente el texto, las páginas en PNG, los assets
  con la transparencia resuelta y la paleta real muestreada de los vectores. Punto de
  partida obligatorio: nunca se maqueta de memoria.
- `qa_maquetacion.py` — holgura al pie en milímetros, cuerpos de texto, degradados sin
  color plano debajo, sombras.
- `qa_fidelidad.py` — demuestra que la remaquetación no tocó ni una palabra.
- `render_paginas.py` — rasteriza el PDF para mirarlo página a página, que es lo único que
  caza los huecos muertos.

## Requisitos

```bash
pip install pymupdf pillow
```

Un Chromium (Edge o Chrome, ya lo tienes) y las fuentes **Poppins** y **Playfair Display**
instaladas en el sistema. Detalle por sistema operativo en `references/toolchain.md`.

## Sin Claude Code

Las referencias se leen igual de bien en papel y los cuatro scripts funcionan sueltos desde
la terminal. Descarga el repo y entra en
`plugins/ico-docs/skills/ico-pdf/`.
