# KUME — Continuación del diseño de pantallas

- **Fecha de traspaso:** 1 de noviembre de 2026
- **Rama de trabajo:** `main`
- **Próximo paso:** diseñar las pantallas y convertir el alcance aprobado en tareas.

## Estado del proyecto

Los pasos 1 a 3 del alcance están completos:

1. Stack tecnológico aprobado.
2. Base de datos, API y almacenamiento de archivos diseñados.
3. Validaciones y reglas técnicas resueltas.

Todavía no se escribió código en frontend ni backend. Tampoco existen pantallas, wireframes o navegación aprobados.

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

MagicPath quedó conectado después de iniciarse la sesión anterior, por lo que no estuvo disponible en ella. La próxima sesión debe verificar que sus herramientas sean visibles y usarlo como espacio principal para:

1. Mapa de navegación.
2. Flujos de usuario.
3. Wireframes de baja fidelidad.
4. Prototipo interactivo revisable.

No sustituir MagicPath por una implementación React antes de que los wireframes sean aprobados.

## Inventario inicial de pantallas por validar

Este inventario es una hipótesis de partida, no una decisión cerrada:

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

Los pasos 1 a 3 ya están completos. El objetivo de esta sesión es ejecutar el paso 4: diseñar las pantallas y convertir el alcance en tareas.

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
