# KUME — Continuación del diseño de pantallas

- **Fecha de traspaso:** 1 de noviembre de 2026
- **Rama de trabajo:** `main`
- **Estado:** paso 4 en curso; sesión pausada por decisión de Maxi.
- **Próxima sesión prevista:** 2 de noviembre de 2026, sujeta a disponibilidad de créditos de MagicPath.
- **Próximo paso:** completar los bocetos de catálogos, revisarlos y continuar con el prototipo interactivo.

## Estado del proyecto

Los pasos 1 a 3 del alcance están completos:

1. Stack tecnológico aprobado.
2. Base de datos, API y almacenamiento de archivos diseñados.
3. Validaciones y reglas técnicas resueltas.

Todavía no se escribió código en frontend ni backend. La estructura de navegación y las tandas de bocetos estáticos de gastos y personal fueron aprobadas por Maxi en esta conversación el 1 de noviembre de 2026. La aprobación parcial no completa el paso 4.

## Avance y decisiones aprobadas — 1 de noviembre de 2026

- Menú lateral con cinco entradas siempre visibles: Gastos, Personal, Rubros, Cursos y Talleres. Trabajo diario y administración se distinguen visualmente.
- Entrada inicial: Gastos del mes actual. Sin dashboard independiente.
- Altas y ediciones de gastos y personal en páginas completas; formularios breves de catálogos previstos en diálogos.
- Orden de revisión: gastos, personal y catálogos.
- Gastos: al guardar, volver al listado conservando filtros y página. Si el gasto queda fuera del filtro, ofrecer «Ver gasto» en el mensaje de éxito.
- Comprobante consultable desde listado y detalle en una pestaña nueva; descarga disponible. Reemplazo como acción independiente desde el detalle, con confirmación.
- Período mediante selector de mes y opción de fechas desde/hasta. Rubro y estado visibles; CSV con los mismos filtros.
- Personal: al crear, abrir la ficha en Datos. Pestañas activas: Datos, Asignaciones y Documentos.
- Pestaña «Marcas de horas» deshabilitada, con «Próximamente». Es una función futura: no agregar registro de horas, endpoints, datos ni integración CLOCK al prototipo actual.
- Conflicto de asignación: mostrar quién ocupa el destino y ofrecer «Ver ficha»; no reemplazar automáticamente. Permitir volver a la ficha original.
- Inactivación: mostrar las asignaciones concretas que se retirarán y solicitar fecha de egreso. Advertir que reactivar no recupera asignaciones.
- Documentos: subir uno por vez, con nombre libre y archivo.
- Gastos anulados y personal inactivo: consulta y descarga, sin edición hasta restaurar o reactivar.
- Las tandas aprobadas incluyen estados vacíos, carga, validación, errores de archivos y confirmaciones. Son bocetos estáticos, no un prototipo interactivo.

### Bocetos aprobados

- G01: listado y filtros de gastos.
- G02: registrar y editar gasto.
- G03: detalle vigente y anulado.
- G04: estados y errores de gastos y archivos.
- G05: confirmaciones y reemplazo.
- P01: listado y búsqueda de personal.
- P02: crear y editar ficha.
- P03: ficha, pestaña Datos.
- P04: asignaciones y conflictos.
- P05: documentos.
- P06: inactivación, ficha inactiva y reactivación.
- P07: estados y errores de personal.

### Pendientes al pausar

1. Completar C01 Rubros, C02 Cursos, C03 Talleres y C04 Estados y bajas bloqueadas. Sus marcos se crearon, pero están vacíos: las llamadas para agregar contenido fueron rechazadas por falta de cuota. No están aprobados.
2. Incluir catálogos inactivos, validaciones y bloqueos de baja o retirada de turnos con asignaciones.
3. Revisar y aprobar los catálogos.
4. Crear y revisar el prototipo interactivo en MagicPath. No confundir las anotaciones de recorrido con interacciones ejecutables; no se implementó React.
5. Documentar las decisiones finales en `screen-design.md`.
6. Preparar el backlog separado de frontend, backend e infraestructura y obtener su aprobación.
7. Marcar el paso 4 como completado únicamente tras confirmación expresa de Maxi; luego commit y push a `main`.

MagicPath informó `EXTERNAL_AGENT_API_QUOTA_EXCEEDED`, con límite y uso de 50 llamadas, sin fecha de reinicio informada. Maxi decidió continuar mañana con nuevos créditos; comprobar disponibilidad en la próxima sesión sin asumir que la cuota se renueva automáticamente.

## Fuentes de verdad

La próxima sesión debe leer estos archivos antes de proponer pantallas:

1. [Alcance del prototipo](alcance-prototipo.md): objetivos, actores, operaciones y exclusiones.
2. [Diseño de API](api-design.md): flujos, estados, errores y comportamiento de cada recurso.
3. [Contrato OpenAPI](openapi.yaml): campos y operaciones exactas.
4. [Diseño de base de datos](database-design.md): entidades, relaciones y estados persistidos.
5. [Stack tecnológico](stack-tecnologico.md): restricciones de implementación.

En caso de contradicción, prevalece el alcance más reciente en `main`; la contradicción debe señalarse antes de diseñar sobre ella.

## Restricciones ya confirmadas

- La usuaria inicial es la secretaria administrativa de KUME y no tiene conocimientos técnicos.
- La aplicación se usa localmente en una computadora y desde un navegador.
- No hay autenticación ni múltiples usuarios en el prototipo.
- No se acordó uso desde celulares; el diseño primario es de escritorio.
- Todos los textos visibles deben estar en español.
- Los valores técnicos de API, como `morning` o `teacher`, se traducen en la interfaz.
- Los archivos admitidos son PDF, JPG y PNG, con máximo de 10 MB.
- No diseñar pantallas de respaldo, restauración ni CLOCK.
- No implementar código durante la fase de wireframes.
- En el repositorio de documentación se trabaja siempre directamente sobre `main`.

## MagicPath

Proyecto existente: **KUME — Diseño administrativo · Paso 4**.

- **projectId:** `467706881381666816`.
- [Abrir proyecto en MagicPath](codex://mcp-app/magicpath@personal/open_magicpath_canvas/projects/467706881381666816).
- Reutilizar este proyecto; no crear otro. Contiene el mapa, G01–G05, P01–P07 y los marcos vacíos C01–C04.
- Respetar las reglas del plugin para abrir o reutilizar el canvas. No consumir llamadas hasta disponer de cuota.
- No sustituir MagicPath por una implementación React antes de completar la aprobación de wireframes.

## Inventario inicial de pantallas por validar

El avance y las aprobaciones de cada tanda se registran arriba. Este es el inventario de referencia:

- Estructura general y navegación.
- Listado de gastos, filtros, total y exportación.
- Alta y edición de gasto con comprobante.
- Detalle de gasto y consulta o reemplazo de comprobante.
- Administración de rubros.
- Listado y búsqueda de personal.
- Alta y edición de ficha de personal.
- Detalle de personal con datos, asignaciones y documentos.
- Administración de cursos.
- Administración de talleres.

No agregar un dashboard independiente salvo que se demuestre que mejora el flujo principal de la secretaria.

## Flujos que el prototipo debe demostrar

1. Registrar un gasto con comprobante.
2. Consultar, filtrar y exportar gastos.
3. Consultar o reemplazar un comprobante.
4. Anular y restaurar un gasto.
5. Crear y administrar rubros.
6. Crear y editar una ficha de personal.
7. Asignar una persona a cursos o talleres y retirar o cambiar la asignación.
8. Subir, consultar, descargar y eliminar documentación del personal.
9. Inactivar y reactivar personal.
10. Administrar e inactivar cursos y talleres respetando sus restricciones.

## Estados y casos que deben aparecer en los bocetos

- Primera utilización sin datos.
- Carga, éxito y error.
- Validaciones de formularios y archivos.
- Confirmaciones para anulación, inactivación y eliminación documental.
- Gastos anulados y personal inactivo en modo de solo lectura.
- Rubros, cursos o talleres inactivos.
- Conflicto de asignación para un destino y turno ocupados.
- Bloqueo de baja cuando un curso o taller conserva asignaciones.
- Archivo demasiado grande o con formato no admitido.

## Resultado esperado del paso 4

Antes de marcar el paso 4 como completo deben existir:

- Mapa de navegación aprobado.
- Wireframes aprobados para todos los flujos del prototipo.
- Comportamiento definido para estados vacíos, errores y confirmaciones.
- Enlace o referencia persistente al proyecto de MagicPath.
- Documento `screen-design.md` con las decisiones finales y referencia a los bocetos.
- Backlog de implementación dividido entre frontend, backend e infraestructura, sin duplicar el contrato OpenAPI.

El paso 4 no debe marcarse como completado hasta que Maxi confirme los wireframes y el backlog.

## Prompt para iniciar la próxima sesión

```text
Continuemos el proyecto KUME desde el repositorio maxifarkuso/kume-admin-docs.

Trabajá siempre sobre la rama main del repositorio de documentación. Antes de proponer cambios, leé completamente:
- alcance-prototipo.md
- continuacion-diseno-pantallas.md
- api-design.md
- openapi.yaml
- database-design.md
- stack-tecnologico.md

Los pasos 1 a 3 están completos y el paso 4 está en curso. Leé primero el avance y las aprobaciones de esta memoria. Reutilizá el proyecto MagicPath 467706881381666816: gastos y personal ya están aprobados. Completá los marcos vacíos de catálogos; después seguí con el prototipo interactivo, screen-design.md y el backlog. No repitas las rondas ya resueltas.

Usá el plugin MagicPath, que ya está conectado, para crear primero un mapa de navegación y luego wireframes de baja fidelidad. No implementes React todavía. Diseñá para una secretaria administrativa sin conocimientos técnicos, uso local en computadora, textos visibles en español y sin pantalla de inicio de sesión.

Usá GrillMe para resolver decisiones reales de UX por rondas, con una recomendación en cada pregunta. No me preguntes hechos que puedas obtener de los documentos. Antes de dibujar todas las pantallas, presentame y recomendame:
1. La arquitectura de información.
2. La navegación principal.
3. El inventario mínimo de pantallas.
4. Los flujos prioritarios que se prototiparán.

Después de mi confirmación, generá en MagicPath los wireframes y el prototipo interactivo. Incluí estados vacíos, carga, error, validación, confirmaciones, gastos anulados, personal inactivo, conflictos de asignación y errores de archivos.

Cuando los wireframes estén aprobados:
- documentá las decisiones en screen-design.md;
- convertí el alcance en un backlog separado para frontend, backend e infraestructura;
- enlazá el proyecto de MagicPath;
- actualizá alcance-prototipo.md y marcá el paso 4 como completado solo con mi confirmación;
- hacé commit y push directamente a main.

No reabras decisiones ya registradas salvo que encuentres una contradicción concreta. Si la encontrás, citá los archivos y pedime decidir antes de continuar.
```
