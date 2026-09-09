# Gráficas

## Orden de preferencia

**1. El vector del cliente.** Si existe un `.ai` o un PDF con la gráfica, se usa ese.
Sale mejor que cualquier reconstrucción y respeta su trabajo.

Un `.ai` guardado con compatibilidad PDF se abre con PyMuPDF y se extrae a SVG:

```python
import fitz
d = fitz.open("grafico.ai"); pg = d[0]

bb = fitz.Rect(1e6, 1e6, -1e6, -1e6)          # recortar al arte, no a la mesa de trabajo
for dr in pg.get_drawings(): bb |= dr["rect"]
for b in pg.get_text("dict")["blocks"]:
    if b["type"] == 0: bb |= fitz.Rect(b["bbox"])
pg.set_cropbox(fitz.Rect(bb.x0-10, bb.y0-10, bb.x1+10, bb.y1+10) & pg.rect)

svg = pg.get_svg_image(text_as_path=True)      # el texto trazado, no como <text>
```

`text_as_path=True` es obligatorio. Con `False`, Chromium no resuelve el nombre de fuente
del PDF ("Poppins-SemiBold"), cae a una serif y rompe el interletrado.

Antes de integrarlo, comprueba a qué cuerpo queda el texto en la página final:
`cuerpo_original × (ancho_final / ancho_del_arte)`. Con 34 pt en un arte de 1335 pt
colocado a 162 mm, quedan 11,7 pt. Por debajo de 9 pt, el gráfico va demasiado reducido.

Consecuencia a avisar: el texto trazado no aparece en la capa de texto del PDF, así que la
prueba de fidelidad no lo ve. Es intencionado.

**2. Redibujarla en SVG.** Solo si no hay vector. Mismo contenido, mejor legibilidad.

## Qué se puede arreglar sin inventar

Rehacer una gráfica del cliente para que se entienda **no** autoriza a añadir información.

Permitido:
- Subir el contraste, agrandar el texto, quitar el fondo de bajo contraste.
- Enderezar etiquetas giradas.
- **Pegar cada etiqueta a lo que nombra** con un punto y una guía. Este es el cambio que
  más rinde: en la curva del olvido, el rótulo del cliente flotaba arriba a la derecha sin
  tocar ninguna curva, y el otro pisaba el "TIEMPO" del eje.
- Separar las zonas con relleno en vez de con líneas.
- Poner el rótulo de una banda dentro de la banda.

No permitido:
- Nombrar series que el cliente dejó sin nombre.
- Añadir marcas de tiempo, leyendas o anotaciones que no estaban.
- Cambiar lo que la gráfica representa. Si su curva de repetición espaciada está
  técnicamente mal dibujada, se reproduce y se comenta aparte.

## Comprobaciones

- Colores de todas las series presentes en la página: `page.get_drawings()`.
- Sin deformar: `preserveAspectRatio` y comparar la proporción con la referencia.
- Que sea vectorial de verdad: `len(page.get_images())` debe ser 0 y
  `len(page.get_drawings())` alto. Si hay una imagen, se ha colado un PNG.
