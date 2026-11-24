# Registro de horas por maestra

Fecha inicial: 16 de noviembre de 2026. Actualización de discovery: 23 de noviembre de 2026. Fuente: decisiones explícitas de Maxi mediante GrillMe en esta conversación y confirmación para crear el prototipo.

Estado: **discovery funcional Q1–Q31 cerrado y confirmado expresamente por Maxi el 23/11/2026; interfaz inicial aprobada**. No acredita implementación, persistencia ni despliegue. Amplía la exclusión histórica de CLOCK para autorizar investigación, definición y diseño; no modifica por sí mismo Personal V1 ni habilita la pestaña del producto desplegado.

## Objetivo y ubicación

Revisar asistencia y horas; liquidación de sueldos fuera de esta etapa. Pantalla dentro del detalle de cada maestra, en la pestaña Registro de horas, con filtro de mes y una fila por día. No se agrega selector de maestra ni un destino principal del menú.

La jornada muestra entrada, salida a almuerzo, regreso y salida final cuando existen dos bloques. Los bloques y pausas deben ser explícitos; no asumir una pausa universal de una hora ni limitar el modelo futuro a exactamente dos bloques. La maqueta ilustra 08:00–12:00 y 13:00–17:00, referencias actuales de cursos. La composición fue aprobada por Maxi el 16/11/2026 y aplica el [sistema visual aprobado](../ui/sistema-visual.md).

## Referencia e interpretación

- Actualización Q2/Q4: la referencia es el horario laboral propio de cada maestra, con bloques por día de la semana y fecha de inicio de vigencia. Sustituye la referencia inicial a horarios de cursos; los cursos quedan como contexto. Contempla tareas como apertura a las 07:30 o ayuda al almuerzo desde las 12:00 aunque el curso corresponda a otro turno. Si no hay horario laboral de referencia, no se infiere entrada o salida.
- Q1: conservar horarios anteriores al cambiar una vigencia. Antes de la primera vigencia registrada se importan marcas sin inferir horario; administración puede cargar una referencia histórica explícita.
- Q8: excepciones por maestra y fecha para licencias, feriados y jornadas especiales. Sustituyen para ese día el horario semanal: sin trabajo previsto no se exigen marcas; una jornada especial define sus propios bloques. Motivo opcional.
- Clock aporta eventos originales; el ejemplo examinado no indica dirección de la marca. El sistema propone una interpretación, sin inventar la hora faltante.
- Ejemplo: bloque 08:00–12:00 y una sola marca a las 12:00 → «Posible salida; falta entrada». La entrada no se completa con 08:00.
- Margen inicial de 60 minutos, configurable por administración, alrededor de cada entrada/salida prevista. Ayuda a asociar eventos, no cambia la hora real ni define tolerancia de puntualidad. Si hay varias interpretaciones posibles, queda por revisar.
- Q6: administración puede asignar marcas del día aunque estén fuera del margen automático, respetando orden temporal y sin reutilizar el mismo evento en dos posiciones.
- Se conservan todas las marcas adicionales o cercanas. Administración asigna las que corresponden, sin descartar automáticamente los originales; el motivo es siempre opcional.
- Un día con horario y sin marcas es «Sin marcas · Por revisar», sin deducir ausencia. Sin bloques previstos es «Sin jornada prevista». Marcas sin referencia son «Sin horario de referencia».
- En una jornada en curso, no se declara faltante hasta pasar la hora esperada más el margen. Antes se muestra «En curso»; bloques futuros, «Pendiente».

## Horas y revisión administrativa

- Resumen mensual separado: horas confirmadas, horas previstas y días por revisar.
- Solo los tramos completos y no ambiguos suman horas confirmadas. Un tramo completo puede sumar aunque otro del mismo día esté incompleto; se identifica como parcial.
- Tramos incompletos no se estiman usando el horario asignado. Las pausas no suman.
- Q23: las marcas heredadas de Clock son inmutables; no permitir corregir su hora, incluso mediante una hora manual sustitutiva. Administración puede asignar originales a posiciones y completar faltantes; las maestras no tienen flujo de propuesta. Esta decisión sustituye cualquier referencia anterior a corregir marcas reales.
- Motivo **opcional en todos los ajustes**, sin categoría ni comentario obligatorio. Se conserva autor, momento e historial antes/después incluso sin motivo.
- Ajustes guardados solamente en KUME, separados de los originales importados. No se escriben correcciones ni asistencias nuevas en Clock.
- Q3/Q5: una nueva marca de Clock reemplaza automáticamente la hora manual utilizada en KUME cuando puede asociarse sin ambigüedad a la misma entrada o salida. Conservar el ajuste anterior y el reemplazo en el historial; no modificar Clock. Si hay varias candidatas, conservar el ajuste y señalar la ambigüedad para revisión.
- Q7: al cambiar retroactivamente un horario, mostrar los días afectados y pedir confirmación antes de recalcular. Conservar originales e historial; los ajustes que dejen de encajar quedan por revisar.

## Comparación informativa de tiempo — Q9 a Q12, 23/11/2026

- Usar la duración real confirmada, sin recortar al horario previsto. No hay decisiones de pago, aprobación de horas pagables, importes ni recargos.
- Mostrar «Tiempo adicional registrado», «Tiempo faltante registrado» y el saldo neto adicional o faltante. Ejemplo: 20 minutos adicionales y 15 faltantes → mostrar ambos componentes y saldo de 5 minutos adicionales. Q10 sustituye la recomendación de no compensar para la presentación del saldo.
- Q9: previsto 07:30–12:00 y registrado 07:25–12:15 → 4 h 50 min reales, 4 h 30 min previstas y 20 minutos adicionales registrados. Q15–Q17 precisan el cálculo y la agregación, según las reglas siguientes.
- Q12: jornada incompleta → «Saldo pendiente de revisión»; conservar las horas confirmadas de tramos completos. El resumen mensual indica saldo parcial y cantidad de días pendientes. No convertir horas desconocidas en tiempo faltante ni en saldo definitivo.

## Precisión, comparación y pausas — Q13 a Q18, 23/11/2026

- Q13: conservar marcas de días sin jornada prevista y solicitar una jornada excepcional antes de calcular su saldo. No considerar automáticamente todo el tiempo como adicional.
- Q14/Q15: nunca mostrar segundos. Truncar cada marca al minuto antes de calcular: 15:00:59 → 15:00. Conservar timestamp original íntegro de Clock para auditoría; no redondear marcas ni saldo hacia arriba. Ejemplo 08:00:59–12:00:01 → 08:00–12:00, cuatro horas.
- Q16: acumular tiempo adicional y faltante de los días resueltos, mostrando ambos y su saldo neto mensual. Ejemplo 40 minutos adicionales y 15 faltantes → 25 adicionales. Indicar parcialidad y días pendientes, según Q12.
- Q17: comparar ubicación temporal del trabajo frente a los bloques previstos, no solo su duración. Previsto 08:00–12:00 y confirmado 08:15–12:15 → cuatro horas trabajadas, 15 minutos adicionales, 15 faltantes y saldo cero. Usar intervalos para evitar doble cómputo entre bloques.
- Q18: con bloques 08:00–12:00 y 13:00–17:00 y solo marcas 08:00 y 17:00, no inferir trabajo durante la pausa. Señalar intermedias faltantes. Administración debe confirmar explícitamente que trabajó sin pausa para resolver ese día.
- Q19: confirmar trabajo durante la pausa modifica los intervalos reales, no la referencia prevista. Mantener ocho horas previstas frente a nueve confirmadas y mostrar una hora adicional registrada, con historial y motivo opcional.

## Horario, ausencias y ambigüedad — Q20 a Q26, 23/11/2026

- Q20/Q21: botón «Horario laboral» dentro de Registro de horas. Precargar los horarios de los cursos asignados exclusivamente para facilitar la carga inicial; administración puede editarlos antes de guardar. Una vez definido, el horario laboral queda independiente: cambios de cursos/asignaciones no lo actualizan ni generan propuestas de actualización. Conservar vigencias al editar posteriormente. Para [CU2](softwareclock/sincronizar-empleado.md), la decisión posterior del 24/11 sustituye esta fuente inicial por el workshift asignado y su definición estructurada en KUME.
- Q22/Q25: permitir «Confirmar que no trabajó» con clasificación Licencia / Enfermedad / Otro y causa de texto libre. Motivo/causa sigue opcional; auditar confirmación. Sin confirmación, ausencia de marcas sigue pendiente y no acredita ausencia.
- Licencia y enfermedad justifican el día sin generar tiempo faltante. «Otro» conserva las horas previstas y registra cero trabajado y el faltante confirmado (ejemplo: ocho horas previstas → ocho faltantes). No determina consecuencias de pago.
- Q24: meses abiertos en esta versión, sin cierre/reapertura ni bloqueo mensual; mantener historial y confirmaciones de cambios retroactivos.
- Q26: ante marca 12:30 con posiciones previstas 12:00 y 13:00 y margen de 60 minutos, no decidir automáticamente por cercanía. Considerar las demás marcas solo si determinan una única combinación válida en orden y sin reutilización; de lo contrario mantener marca sin asignar para revisión administrativa.

## Margen y egreso — Q27 a Q31, 23/11/2026

- Q27: margen general de KUME, inicialmente 60 minutos y editable por administración, sin configuración individual por maestra en esta versión. No modifica horas reales ni define puntualidad.
- Q28: cada cambio de margen tiene fecha de vigencia y conserva la interpretación histórica. Reprocesar días anteriores requiere vista de afectados y confirmación, conservando originales e historial.
- Q29/Q30: administración puede consultar y resolver jornadas históricas de una ficha inactiva sin reactivarla. El egreso es inclusivo: ese día puede tener jornada prevista; desde el siguiente no se generan horas previstas ni faltantes. Una excepción permite justificar el último día.
- Q31: conservar marcas posteriores al egreso como «Marca posterior al egreso · Por revisar», excluidas automáticamente de horas trabajadas, previstas y diferencias. No reactivar la ficha. Administración puede detectar una fecha incorrecta o marca inesperada; el eventual cambio de egreso se rige por su operación explícita y no se deduce de la marca.

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

1. Diseñar persistencia de horarios laborales propios con vigencias y excepciones según Q1/Q4/Q7/Q8; Personal V1 no incluye ese modelo. No reinterpretar meses anteriores con el horario actual.
2. Editor «Horario laboral» en Registro de horas (Q20). Margen general con vigencias aprobado en Q27/Q28; concretar persistencia y editor conforme estas reglas. La extensión a otros roles no está incluida por inferencia.
3. Especificar algoritmo conforme Q26: interpretar automáticamente solo si existe una única combinación válida, respetando orden y sin reutilizar eventos; ambigüedad exige revisión, sin elegir por cercanía.
4. Definir persistencia de eventos, ajustes y auditoría, identidad de marca, control de concurrencia y tratamiento de cambios/tardíos de Clock.
5. Diseñar contrato interno KUME, errores, caché y actualizaciones, ampliar OpenAPI/base y sincronizar consumidores antes de desarrollar. No hay endpoints internos aprobados en esta sesión.
6. Validar zona horaria y precisión de Clock, límites de consulta, fechas inclusivas, token y fallos reales según [hallazgos de integración](../technical/softwareclock-api.md).
7. Preparar especificaciones funcional y técnica, plan y tareas usando la interfaz aprobada. La aprobación de esta pantalla no cierra el paso 4 general. Consultar la [guía para especificar y conectar](../technical/registro-horas-preparacion.md).

Ver [maqueta y verificaciones](../ui/maquetas/registro-horas/README.md).

## Confirmación de interfaz — 16 de noviembre de 2026

Maxi expresa «me gusta mucho la interfaz» y solicita documentar todas las decisiones para comenzar las especificaciones y la conexión con Clock. Se registra como aprobación visual del prototipo identificado en la [memoria de maqueta](../ui/maquetas/registro-horas/README.md). No reabrir composición, ubicación ni acuerdos de GrillMe al preparar especificaciones. Las restricciones de demostración y los pendientes técnicos no se convierten por esa aprobación en reglas de producción.

## Cierre funcional y especificación — 23/11/2026

Maxi confirma el cierre funcional y avanzar a especificaciones y plan manteniendo las validaciones técnicas de Clock pendientes. La [iniciativa 010](../specs/010-time-records/spec.md) formaliza criterios de aceptación; [propuesta técnica](../specs/010-time-records/technical-spec.md), [plan](../specs/010-time-records/plan.md) y [tareas/evidencia](../specs/010-time-records/tasks.md) preparan la implementación. No acredita aprobación de contratos públicos nuevos ni implementación. El paso 4 general conserva su estado.

## Ampliación solicitada tras cierre — vinculación y catálogo Clock

El 23/11 Maxi pide botón «Sincronizar empleado con Clock» en ficha y apartado administrativo para importar horarios laborales externos. La muestra real de estructura de turnos solo aporta código/nombre/tipo, sin bloques calculables. [Diseño y secuencias](../technical/softwareclock-employee-mapping.md). La importación del catálogo no cambia horarios laborales ya definidos; completar estructura local y usarla como plantilla es una propuesta a confirmar. La aprobación del cierre anterior no cubre automáticamente el diseño visual o contrato de este apartado nuevo.
