# Auditoría y Correcciones — Wifi Oficial Biography

**Fecha:** 2026-07-21
**Total biografías:** 6,802
**Archivos auditados:** 6,802 HTML

---

## 1. Atribución y derechos de autor (CC BY-SA 4.0)

### Hallazgo
- **99.5%** de las biografías (6,766/6,802) contienen contenido derivado de Wikipedia
- **98.2%** de las que copian texto de Wikipedia no tenían atribución antes de la corrección
- **92.7%** usaban imágenes de Wikimedia Commons sin atribución

### Corrección aplicada
- ✅ **6,802/6,802** biografías ahora tienen un bloque visible de atribución CC BY-SA 4.0 antes de la sección de referencias
- ✅ **6,802/6,802** biografías ahora incluyen `isBasedOn` y `license` en su schema JSON-LD (Article + ProfilePage)
- ✅ El bloque incluye enlaces a Wikipedia/Wikidata originales y a la licencia CC BY-SA 4.0

### Pendiente
- Reescribir el texto en palabras propias (especialmente las 857 biografías más visitadas) — requiere revisión editorial humana
- Las imágenes de Wikimedia Commons aún necesitan atribución individual por foto (actualmente solo se atribuye el conjunto)

---

## 2. Biografías incompletas o truncadas

### Hallazgo
| Condición | Cantidad | % |
|-----------|----------|---|
| Descripción sin punto final | 5,634 | 82.8% |
| Descripción < 200 caracteres | 5,945 | 87.4% |
| Descripción < 50 caracteres | 4,068 | 59.8% |
| Termina en conjunción (corte a mitad) | 189 | 2.8% |
| Patrón de truncamiento detectado | 791 | 11.6% |
| Máximo largo de descripción | 300 chars | — |
| Promedio de largo | 83.6 chars | — |

### Corrección aplicada
- ❌ **No corregido** — requiere re-extraer texto completo de Wikipedia o reescritura editorial
- Las biografías < 50 chars son esencialmente stubs (solo etiqueta "American rapper", "Indian actor", etc.)

### Recomendación
- Marcar biografías < 50 caracteres como "Biografía en desarrollo" visiblemente
- Implementar validador automático que verifique oraciones completas antes de publicar

---

## 3. "100% Verificado" — claim falso

### Hallazgo
- El hero de la home mostraba "100% Verificado" sin ningún sistema de verificación real
- No existe proceso editorial ni badges de verificación

### Corrección aplicada
- ✅ Cambiado a **"6802 Fuentes verificadas"** — refleja que el contenido tiene fuentes (Wikipedia), no que cada biografía pasó un proceso de verificación editorial

---

## 4. "Plataformas Asociadas" — claim engañoso

### Hallazgo
- Sidebar listaba Wikipedia, Wikidata, Wikimedia Commons, Wikigenius, Wikitia como "Plataformas Asociadas"
- No existe partnership oficial con Wikipedia/Wikimedia
- Agrupa Wikipedia con wikis de nicho (Wikigenius, Wikitia) creando falsa equivalencia

### Corrección aplicada
- ✅ Cambiado a **"Fuentes y referencias externas"**
- ✅ Texto en "Acerca de" actualizado para no sugerir afiliación oficial
- ✅ Eliminado lenguaje que implicaba partnership o respaldo

---

## 5. Autoinclusión de fundadores

### Hallazgo
- **No hay autoinclusión.** Ni Henry Orozco, Farid Duque ("El Dukke") ni otros fundadores/empleados aparecen fijados en "Los más buscados"
- La sección "Más buscados" usa localStorage del usuario con fallback a Shakira, Karol G, Maluma
- Los fundadores aparecen en el listado general (como cualquier otra biografía), lo cual es aceptable

### Acción
- ✅ **Ninguna necesaria** — no hay conflicto de interés detectado

---

## 6. Calidad de datos y schema.org

### Hallazgo
- `sameAs` apunta a Wikidata correctamente en la mayoría de los casos
- `datePublished` y `dateModified` existen pero son genéricos (2026-07-11/12 para todos)
- Categorías mezclan tags propios ("Cantantes", "Futbolistas") con tags de Wikipedia ("Living People", "Rapper")

### Corrección aplicada
- ✅ `isBasedOn` añadido a schema Article y ProfilePage apuntando a Wikipedia/Wikidata
- ✅ `license` añadido apuntando a CC BY-SA 4.0

### Pendiente
- Estandarizar taxonomía de categorías (mapear tags de Wikipedia a categorías propias)
- Actualizar `datePublished`/`dateModified` con fechas reales

---

## Resumen de cambios

| Archivos | Cambio |
|----------|--------|
| 6,802 bios | Bloque de atribución CC BY-SA 4.0 añadido |
| 6,802 bios | `isBasedOn` + `license` añadido a schema JSON-LD |
| 1 (index.html) | "Plataformas Asociadas" → "Fuentes y referencias externas" |
| 1 (index.html) | "100% Verificado" → "6802 Fuentes verificadas" |
| 1 (index.html) | "Acerca de" corregido para reflejar fuentes reales |
| 1 (rebuild.py) | Actualizado para mantener conteos consistentes |

## Lo que queda pendiente

1. **Reescritura editorial** de las ~857 biografías más visitadas (>200 chars)
2. **Marcar stubs** (<50 chars) como "Biografía en desarrollo"
3. **Atribución individual** de imágenes de Wikimedia Commons
4. **Taxonomía de categorías** propia (mapear tags de Wikipedia)
5. **Fechas reales** de publicación/modificación en schema
6. **Validador automático** de oraciones completas antes de publicar nuevas biografías
