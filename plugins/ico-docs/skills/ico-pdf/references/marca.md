# Sistema visual ICO para documento impreso

Todos los valores están muestreados de PDFs reales aprobados por el cliente, no inventados.
Si dudas de un color, sácalo del PDF del cliente con `page.get_drawings()`.

## Color

| Uso | Hex |
|---|---|
| Titulares, `<strong>`, pastillas | `#172B8F` |
| Cuerpo de texto | `#4D5872` |
| Azul de acción (filetes, antetítulos, borde de callout) | `#1A52D8` |
| Azul claro (acentos sobre fondo oscuro) | `#6DB8FF` |
| Azul del isotipo | `#0068FF` |
| Panel lavanda (apertura, callouts) | `#EDF2FD` |
| Caja de tip | `#F1F5FE` |
| Filetes y retícula | `#DFE9FB` · `#CFE0FF` · `#E5E9F2` |
| Gris apagado (pies, folios) | `#A9B0C4` |
| Dorado (subtitulares de cierre) | `#F1C86A` |

**Degradado de portada y cierre**
`linear-gradient(135deg, #1982DE 0%, #1242A8 30%, #12297A 62%, #0A1636 100%)`

Siempre con un color plano debajo. Ver `toolchain.md`, sección degradados.

**Series de gráficas** (orden de peor a mejor retención)
`#6DB8FF` · `#37B0A6` · `#3F6BD6` · `#F2B134`

## Tipografía

**Playfair Display 700 — solo titulares.** Nunca en cuerpo, pastillas ni etiquetas.
Nunca en mayúsculas: "La atención plena", no "LA ATENCIÓN PLENA".

**Poppins — todo lo demás.** Light 300 para cuerpo, 500/600 para etiquetas y antetítulos.

| Elemento | Cuerpo | Notas |
|---|---|---|
| Titular de portada | 54 pt | 2–3 líneas, `line-height` 1,05 |
| Titular de cierre | 44 pt | |
| Titular de sección | 19–21 pt | Playfair 700, `line-height` 1,14 |
| Subtitular de cierre | 19,5 pt | Playfair, en dorado |
| Cuerpo | **11,5 pt** | `line-height` 1,54–1,65. Mínimo absoluto |
| Texto de callout | 11 pt | |
| Antetítulo / etiqueta | 8,6 pt | Versalitas, `letter-spacing` 2,2–2,4 px, en azul |
| Pie y folio | 8,5 pt | Suelo del documento |

**Patrón firmado: última palabra del titular en itálica y azul.**
`Diseña tu día para entrar en <i>flow</i>` · `Ponle un límite a <i>todo</i>`
Sobre fondo oscuro la itálica va en `#6DB8FF`; sobre fondo claro, en `#1A52D8`.

Ojo con las tildes en titulares grandes: comprueba que no invadan la línea superior.

## Retícula A4

```
Página            210 × 297 mm
Márgenes          18 mm laterales · 17 mm superior · 19,5 mm inferior
Columna de texto  174 mm
Pie               filete a 10,5 mm del borde inferior
Holgura mínima    3,5 mm entre el último píxel de contenido y el filete del pie
```

La holgura se mide con `qa/qa_maquetacion.py`. A ojo no se ve: una caja de callout puede
quedar a 1 mm del filete y parecer correcta en pantalla.

## Componentes

**Cabecera de marca** (portada y cierre, nunca en interiores)
Isotipo de 20 mm + "Instituto de / Comunicación" en Playfair 16 pt, arriba a la izquierda,
con filete a todo el ancho debajo.

**Apertura**
Bloque macizo en `#172B8F` con el texto en `#D8E2F7`. Ancla la primera página y da peso.

**Antetítulo de sección**
Barra azul de 9 mm × 2,6 px + etiqueta en versalitas + filete fino hasta el margen derecho.
Debajo, el titular en Playfair.

**Callout / tip**
Fondo `#EDF2FD`, borde izquierdo de 3 px en `#1A52D8`, etiqueta en versalitas azules en
línea con el texto. Sin emoji, sin icono decorativo.

**Figura**
Tarjeta con borde `#DFE9FB` y, si la figura tiene título en el original, banda superior
en navy con el título en Playfair blanco.

**Pie**
Filete `#E5E9F2` + "Instituto de Comunicación" centrado + folio a la derecha, ambos en
`#A9B0C4` a 8,5 pt.

## Prohibiciones

- Sombras de cualquier tipo. Para legibilidad sobre foto se usa un scrim de fondo.
- Recortar imágenes de contenido. Se escala el contenedor o se recompone la página.
- Isotipos pequeños sueltos en esquinas de páginas interiores.
- Highlights con fondo de color sobre palabras sueltas. Solo `<strong>` en navy.
- Playfair en mayúsculas.
- Emojis decorativos.
