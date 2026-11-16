# Registro de horas por maestra

Fecha: 16 de noviembre de 2026. Fuente: decisiones explícitas de Maxi mediante GrillMe en esta conversación y confirmación para crear el prototipo.

Estado: **reglas funcionales e interfaz aprobadas por Maxi**. No acredita implementación, persistencia ni despliegue. Amplía la exclusión histórica de CLOCK para autorizar investigación, definición y diseño; no modifica por sí mismo Personal V1 ni habilita la pestaña del producto desplegado.

## Objetivo y ubicación

Revisar asistencia y horas; liquidación de sueldos fuera de esta etapa. Pantalla dentro del detalle de cada maestra, en la pestaña Registro de horas, con filtro de mes y una fila por día. No se agrega selector de maestra ni un destino principal del menú.

La jornada muestra entrada, salida a almuerzo, regreso y salida final cuando existen dos bloques. Los bloques y pausas deben ser explícitos; no asumir una pausa universal de una hora ni limitar el modelo futuro a exactamente dos bloques. La maqueta ilustra 08:00–12:00 y 13:00–17:00, referencias actuales de cursos. La composición fue aprobada por Maxi el 16/11/2026 y aplica el [sistema visual aprobado](../ui/sistema-visual.md).

## Referencia e interpretación

- La referencia proviene de los cursos asignados en KUME, con días y horas; no de los turnos de Clock. Si no hay horario de referencia, no se infiere entrada o salida.
- Clock aporta eventos originales; el ejemplo examinado no indica dirección de la marca. El sistema propone una interpretación, sin inventar la hora faltante.
- Ejemplo: bloque 08:00–12:00 y una sola marca a las 12:00 → «Posible salida; falta entrada». La entrada no se completa con 08:00.
- Margen inicial de 60 minutos, configurable por administración, alrededor de cada entrada/salida prevista. Ayuda a asociar eventos, no cambia la hora real ni define tolerancia de puntualidad. Si hay varias interpretaciones posibles, queda por revisar.
- Se conservan todas las marcas adicionales o cercanas. Administración asigna las que corresponden, sin descartar automáticamente los originales; el motivo es siempre opcional.
- Un día con horario y sin marcas es «Sin marcas · Por revisar», sin deducir ausencia. Sin bloques previstos es «Sin jornada prevista». Marcas sin referencia son «Sin horario de referencia».
- En una jornada en curso, no se declara faltante hasta pasar la hora esperada más el margen. Antes se muestra «En curso»; bloques futuros, «Pendiente».

## Horas y revisión administrativa

- Resumen mensual separado: horas confirmadas, horas previstas y días por revisar.
- Solo los tramos completos y no ambiguos suman horas confirmadas. Un tramo completo puede sumar aunque otro del mismo día esté incompleto; se identifica como parcial.
- Tramos incompletos no se estiman usando el horario asignado. Las pausas no suman.
- Solo administración puede agregar, corregir o asignar marcas. Las maestras no tienen flujo de propuesta en esta etapa.
- Motivo **opcional en todos los ajustes**, sin categoría ni comentario obligatorio. Se conserva autor, momento e historial antes/después incluso sin motivo.
- Ajustes guardados solamente en KUME, separados de los originales importados. No se escriben correcciones ni asistencias nuevas en Clock.
- Una nueva importación debe conservar ajustes e historial. Si aparecen marcas tardías que chocan con un ajuste, la resolución debe ser explícita; política detallada pendiente antes de implementar.

## Consulta y actualización

Consultar Clock al abrir el apartado o cambiar el mes. Mostrar última actualización y botón Actualizar. Ante error conservar datos de la última consulta, señalarlos como desactualizados y ofrecer reintento manual; nunca confundir error con ausencia de marcas. No se aprobó sincronización programada.

Las marcas pueden llegar más tarde por sincronización offline según la [FAQ oficial de Clock](https://softwareclock.com/faqs/). Esa condición obliga a reevaluar incidencias tras nuevas importaciones; el motivo concreto del retraso no puede deducirse solo de dos timestamps.

## Estados de interfaz

| Estado | Presentación |
| --- | --- |
| Completo | Tramos completos y sin ambigüedades pendientes |
| Ajustado | Jornada resuelta con intervención administrativa identificable |
| Por revisar | Marca faltante, marcas ambiguas o excedentes no resueltos |
| Sin marcas | Detalle de un día previsto sin eventos; no equivale a ausencia |
| Sin horario de referencia | Eventos que no pueden interpretarse automáticamente |
| Sin jornada prevista | No existen bloques asignados para el día |
| En curso / Pendiente | Faltantes aún no vencidos / bloques futuros |
| Cargando / Error / Sin datos | Estados de consulta independientes del estado de asistencia |

## Pendientes antes de implementar

1. Diseñar vigencia histórica de horarios/asignaciones: Personal V1 conserva asignaciones actuales, sin historial. No reinterpretar meses anteriores usando silenciosamente el horario vigente de hoy.
2. Concretar la configuración de bloques y pausas, su persistencia y el alcance de la configuración del margen. Los talleres solo tienen días y turno en el modelo actual; su horario exacto y la extensión a otros roles no están incluidos por inferencia.
3. Definir algoritmo ante candidatos que se solapan; 60 minutos puede incluir dos fronteras de bloques cercanos. No elegir el más cercano silenciosamente sin validar la regla.
4. Definir persistencia de eventos, ajustes y auditoría, identidad de marca, control de concurrencia y tratamiento de cambios/tardíos de Clock.
5. Diseñar contrato interno KUME, errores, caché y actualizaciones, ampliar OpenAPI/base y sincronizar consumidores antes de desarrollar. No hay endpoints internos aprobados en esta sesión.
6. Validar zona horaria y precisión de Clock, límites de consulta, fechas inclusivas, token y fallos reales según [hallazgos de integración](../technical/softwareclock-api.md).
7. Preparar especificaciones funcional y técnica, plan y tareas usando la interfaz aprobada. La aprobación de esta pantalla no cierra el paso 4 general. Consultar la [guía para especificar y conectar](../technical/registro-horas-preparacion.md).

Ver [maqueta y verificaciones](../ui/maquetas/registro-horas/README.md).

## Confirmación de interfaz — 16 de noviembre de 2026

Maxi expresa «me gusta mucho la interfaz» y solicita documentar todas las decisiones para comenzar las especificaciones y la conexión con Clock. Se registra como aprobación visual del prototipo identificado en la [memoria de maqueta](../ui/maquetas/registro-horas/README.md). No reabrir composición, ubicación ni acuerdos de GrillMe al preparar especificaciones. Las restricciones de demostración y los pendientes técnicos no se convierten por esa aprobación en reglas de producción.
