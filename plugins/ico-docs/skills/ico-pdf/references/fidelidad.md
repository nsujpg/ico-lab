# Fidelidad de contenido

## La regla

Cuando el encargo es **adaptar material que ya existe**, el contenido va íntegro y exacto.

Prohibido: resúmenes propios, tablas comparativas de cosecha propia, cajas de "consejos",
renumerar, reordenar apartados, corregir erratas por tu cuenta.

Se respetan títulos, numeración, orden y hasta las erratas del original.

## Por qué

Convierte una adaptación en una reinterpretación. El material es del cliente. En ICO ya
costó una ronda con unos apuntes donde se habían añadido una tabla resumen, una caja
"Ojo al detalle" y bullets introductorios.

## Erratas e incoherencias

Se reproducen tal cual **y se comentan aparte en el mensaje de entrega**. Nunca se corrigen
dentro del documento sin permiso.

Ejemplo real de la Guía de productividad ilegal: el gráfico que dibujó el cliente decía
"La falta de repaso **puedo** provocar una **caida**". Se maquetó tal cual y se avisó en
el mensaje con las dos correcciones propuestas.

## Lo que sí es maquetación y no toca el contenido

- Partir un titular por su propia raya: `Paso 1 — La mentalidad del 1%` se compone como
  antetítulo `PASO 1` + titular `La mentalidad del 1%`. Las palabras siguen todas ahí; el
  separador pasa a ser un cambio de nivel tipográfico. **Avísalo igualmente al entregar.**
- Repaginar para equilibrar las páginas, sin cambiar el orden.
- Cambiar el tipo de letra, el color o el tamaño.

## Cómo demostrarlo

```bash
python qa/qa_fidelidad.py "original.pdf" "rediseño.pdf"
```

Compara la **secuencia de palabras** de los dos PDFs con `difflib.SequenceMatcher`.
A nivel de frase da falsos positivos por los saltos de línea; a nivel de palabra es fiable.

El informe separa las diferencias reales de los artefactos conocidos:

- Etiquetas con `letter-spacing` salen letra a letra ("T Ú  P U E D E S").
- Las etiquetas de eje de una gráfica salen en otro orden de lectura.
- El texto vectorizado de una figura no aparece en la capa de texto.
- Pies de página y folios.

Una similitud del 0,93 con todas las diferencias explicadas es un pase. Una del 0,99 con
una diferencia real no lo es. Lee la lista, no el número.
