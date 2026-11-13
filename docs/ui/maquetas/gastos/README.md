# Maqueta visual de Gastos — Dirección B

Fecha: 13 de noviembre de 2026. **Composición visual aprobada por Maxi, con ajuste solicitado al menú lateral**.

Los acuerdos del diseño pertenecen a [Sistema visual y piloto de Gastos](../../sistema-visual.md). Esta carpeta conserva su representación visual y el código de referencia de la maqueta; no es código para instalar directamente en el frontend.

## Ubicación y contenido

- Proyecto MagicPath existente: `467706881381666816`, KUME — Diseño administrativo · Paso 4.
- Componente nuevo: `471969298420756480`, «Gastos · Dirección B · Piloto visual».
- Revisión comprobada: `471975249806766080`.
- Nombre generado: `fresh-pond-8285`.
- Los bocetos G01–G05 y el resto del proyecto se conservan.

La franja superior «Revisión visual» permite alternar Listado, Formulario y Detalle. En Listado se pueden revisar carga, primer uso, filtros sin resultados, error y éxito. El formulario permite probar validación, importe, selección de archivo y guardado ficticio. El detalle permite probar confirmaciones y anulación/restauración. Las opciones de estado son controles de revisión, no forman parte de la navegación del producto. Los módulos ajenos a Gastos y cierre de sesión están deshabilitados solamente en esta maqueta.

| Pantalla | Captura |
| --- | --- |
| Listado, filtros, total y tabla | [listado.png](listado.png) |
| Formulario y comprobante seleccionado | [formulario.png](formulario.png) |
| Detalle en dos columnas | [detalle.png](detalle.png) |
| Gasto anulado | [anulado.png](anulado.png) |

Fuentes de la maqueta: [componente React](GastosDirecciNBPilotoVisual.tsx) y [estilos](GastosDirecciNBPilotoVisual.css). Se incluyen para conservar el trabajo de diseño. La futura implementación debe adaptar los componentes a la arquitectura y formularios existentes, mantener contratos y pruebas del producto, y evitar copiar la orquestación ficticia.

## Límites y propuestas de composición

Datos, fechas y archivos son ficticios. No hay API, autenticación, persistencia, verificación real de firma de archivos ni prueba de integración. El ejemplo abre/descarga un archivo de texto ficticio; el bloque PDF representa la apariencia propuesta, no un visor PDF implementado. Los metadatos visuales son de ejemplo y no están sincronizados con los archivos elegidos.

La paginación muestra una única página. Fecha y mes usan controles nativos, cuya presentación depende del navegador y su configuración regional; las capturas locales usan `es-UY`. Noviembre de 2026 y el día 13 están fijados solo para la demostración. La aplicación implementada debe conservar el día de negocio America/Montevideo.

Para aprovechar el espacio de la maqueta se muestran destinatario y concepto en dos líneas dentro de una misma columna; es una composición incluida en la aprobación visual del piloto, conserva ambos datos y no cambia el modelo ni el CSV. La aprobación visual comprende la composición presentada; no agrega una nueva identidad de marca institucional. Las filas crecen para acomodar las dos líneas.

## Verificaciones realizadas

- Compilación de las revisiones en MagicPath: completada.
- Altura final de filtros verificada en Chromium: 44 px en mes y selectores, y también en Desde/Hasta al elegir período personalizado. Captura de listado actualizada.
- Ajuste de menú verificado en Chromium: sin borde izquierdo y opciones 8 px más angostas; cabezal de revisión visible. Capturas actualizadas.
- Captura remota inspeccionada para revisar correspondencia de paleta y jerarquía; capturas locales de las tres pantallas y anulado inspeccionadas a 1440 px.
- Comprobaciones de comportamiento en Chromium local: listado; tarjeta de total cerrada al recibir foco, apertura con clic y cierre con Escape; validación y foco del primer error; ingreso `132050` → `1320,50`; Retroceso → `132,05`; seleccionar todo y reemplazar; pegado de `1320,50`, `1320.50` y `132050`; selección de archivo; diálogo de salida; guardado ficticio; detalle; confirmación y anulación; estados de carga, vacío, primer uso y error. Sin errores JavaScript de página durante el recorrido.
- Estas comprobaciones se ejecutaron con herramientas aisladas en `work/`; no se incorporaron dependencias de producción ni herramientas de prueba al frontend.
- Contraste calculado: azul/blanco 7,10:1; texto principal/blanco 12,95:1; texto secundario/blanco 6,31:1; borde de control/blanco 3,25:1. Textos de éxito, error y advertencia sobre sus fondos: 6,53:1, 6,73:1 y 6,67:1, respectivamente.
- No es una auditoría completa WCAG: faltan lector de pantalla, zoom, matriz de navegadores/sistemas y verificación integrada de estados y archivos. Maxi aprobó visualmente el piloto con los ajustes de menú documentados.

## Continuación

La revisión visual del piloto está aprobada. Se conserva el cabezal de herramientas de maqueta por pedido expreso de Maxi: no es UI de producto. Se quitó el borde azul lateral y se redujeron 8 px las opciones del menú (4 px por lado). Preparar el plan de implementación y extensión como siguiente etapa. No marca completo el paso 4.
