# Registro de horas — Especificación funcional

> **Separación para continuar:** esta iniciativa corresponde a [CU3 Registro de horas](../../functional/softwareclock/registro-horas.md). La vinculación se trata en [CU2](../../functional/softwareclock/sincronizar-empleado.md) y el catálogo en [CU1](../../functional/softwareclock/sincronizar-horarios.md). [Prompts y dependencias](../../functional/softwareclock/README.md).

Fecha: 23 de noviembre de 2026. Estado: discovery funcional Q1–Q31 cerrado expresamente por Maxi. Este documento traduce las [reglas propietarias](../../functional/registro-horas.md) a criterios verificables; ante discrepancia, reconciliar con esas decisiones. Diseño técnico propuesto en [technical-spec.md](technical-spec.md), ejecución en [plan.md](plan.md) y [tasks.md](tasks.md).

No acredita implementación ni integración productiva. La interfaz inicial fue aprobada el 16/11; las ampliaciones de discovery requieren adaptación, sin reabrir su composición general. Los hechos del proveedor siguen pendientes de validación.

## Objetivo, actores y alcance

Administración revisa asistencia de cada maestra, resuelve faltantes y compara tiempo trabajado con previsto. Ubicación: ficha → Registro de horas. Sin selector de maestra ni nuevo destino principal. Maxi y Vicky conservan sus permisos administrativos; las maestras no son nuevas cuentas del sistema.

Se incluyen horario laboral propio con vigencias, excepciones por fecha, importación de Clock, interpretación, revisión, auditoría y comparación informativa. Se excluyen liquidación, recargos, aprobación de pago, cierre mensual, escritura en Clock, sincronización programada y extensión automática a otros roles.

## Vocabulario de la funcionalidad

| Término | Significado |
| --- | --- |
| Marca original | Evento recibido de Clock; fecha/hora original inmutable en KUME |
| Posición esperada | Entrada o salida de un bloque laboral previsto |
| Hora manual | Hora registrada por administración para completar una posición faltante; no sustituye una marca real existente |
| Intervalo confirmado | Trabajo con inicio y fin válidos; puede provenir de originales, faltantes completados o confirmación explícita sin pausa |
| Horario laboral | Bloques semanales propios de la maestra, independientes de cursos después de su definición inicial |
| Vigencia | Fecha desde la que aplica una referencia de horario o margen, conservando anteriores |
| Jornada excepcional | Referencia por fecha que sustituye el horario semanal para ese día |
| Adicional / faltante | Minutos confirmados fuera / dentro del horario previsto sin trabajo, respectivamente; no son decisiones salariales |
| Saldo | Adicional menos faltante; indica dirección, no importe ni autorización de pago |

## Criterios de aceptación

| ID | Comportamiento verificable | Discovery |
| --- | --- | --- |
| AC01 | Mes por defecto actual del negocio America/Montevideo; una fila por día, bloques, marcas y estado; conservar contexto al revisar | Vista aprobada |
| AC02 | El horario propio se puede editar antes de guardar y queda independiente. En [CU2](../../functional/softwareclock/sincronizar-empleado.md) la precarga inicial usa la definición estructurada del workshift asignado | Q2, Q4, Q20–Q21 |
| AC03 | Bloques por día de semana y vigencia; antes de la primera referencia, importar sin inferir; permitir carga histórica explícita | Q1, Q4 |
| AC04 | Excepción por maestra/fecha para licencia, enfermedad, feriado o jornada especial, con causa opcional; mantener horario semanal histórico | Q8, Q22, Q25 |
| AC05 | Cambio retroactivo de horario muestra afectados y exige confirmación; conserva originales e historial y deja ajustes incompatibles por revisar | Q7 |
| AC06 | Margen general inicial 60 minutos con vigencias; reproceso histórico exige vista previa y confirmación; no define puntualidad | Q27–Q28 |
| AC07 | Proponer asignación solo con una única combinación válida en orden y sin reutilizar eventos; varias candidatas quedan sin resolver; no elegir por cercanía | Q26 |
| AC08 | Administración puede asignar originales fuera del margen, en orden y sin reutilizarlos; nunca editar su fecha/hora | Q6, Q23 |
| AC09 | Completar posiciones sin marca con horas manuales y motivo opcional; conservar actor, instante y antes/después | Q3, Q5 y regla administrativa |
| AC10 | Una marca nueva inequívoca para ese faltante sustituye la hora manual usada, con historial; con varias candidatas conservar manual e incidencia | Q3, Q5 |
| AC11 | No descartar duplicados/cercanas automáticamente ni permitir ocultar una marca real mediante una sustitución manual | Q23, Q26 |
| AC12 | No inferir entrada por horario previsto ni ausencia por falta de eventos; esperar hora esperada más margen antes de declarar faltante; futuros pendientes | Reglas iniciales |
| AC13 | Sumar solo intervalos completos no ambiguos; identificar parcialidad; ningún tramo desconocido se estima | Q12 |
| AC14 | Truncar segundos de cada marca para visualización y cálculo; guardar original íntegro; interfaz nunca muestra segundos | Q14–Q15 |
| AC15 | Diferencias por ubicación temporal de intervalos, no solo duración; mostrar adicional, faltante y saldo diario y mensual | Q9–Q10, Q16–Q17 |
| AC16 | Día incompleto: saldo pendiente; mes parcial y cantidad de días pendientes; sus horas confirmadas siguen visibles | Q12, Q16 |
| AC17 | Dos extremos del día no acreditan trabajo durante pausa; exigir confirmación expresa para intervalo continuo, manteniendo referencia prevista | Q18–Q19 |
| AC18 | Marcas sin jornada: conservar y pedir jornada excepcional antes de calcular saldo; sin referencia histórica: no inferir | Q1, Q13 |
| AC19 | Confirmar que no trabajó permite Licencia / Enfermedad / Otro y causa opcional; las primeras no generan faltante; Otro registra 0 trabajado y faltante previsto | Q22, Q25 |
| AC20 | Meses abiertos; permitir revisión histórica de inactivas sin reactivación; egreso inclusivo y desde el día siguiente sin jornada esperada | Q24, Q29–Q30 |
| AC21 | Evento posterior al egreso se conserva como Por revisar, excluido de trabajo, previstos y diferencias automáticos; no reactiva ficha | Q31 |
| AC22 | Consulta al abrir/cambiar mes y Actualizar; última consulta visible; error conserva última lectura exitosa como desactualizada, sin inferir ausencia | Reglas iniciales |
| AC23 | Ninguna operación escribe en Clock; credenciales/token solo backend; cada operación exige sesión y respeta protección de escritura existente | Alcance y arquitectura |
| AC24 | Edición concurrente no sobrescribe trabajo ajeno; error conserva borrador; horarios, excepciones, revisión e importación mantienen coherencia | Control optimista vigente |
| AC25 | Para una maestra sin vínculo confirmado, Registro de horas está deshabilitado y remite a «Sincronizar empleado con Clock» en Datos | Continuación CU3 |
| AC26 | Tras confirmar CU2, la pestaña se habilita en la misma ficha sin recarga manual y abre al seleccionarla | Continuación CU3 |
| AC27 | Con vínculo confirmado y horario pendiente, permite abrir y consultar marcas; el cálculo que requiere horario queda pendiente | Continuación CU3 |
| AC28 | Un vínculo existente en revalidación conserva acceso al historial disponible, explica cómo revalidar en Datos y bloquea nuevas importaciones; se conserva la revisión histórica de inactivas | Continuación CU3 |

## Ejemplos obligatorios de cálculo

| Previsto | Confirmado | Trabajo | Adicional | Faltante | Saldo |
| --- | --- | --- | --- | --- | --- |
| 07:30–12:00 | 07:25–12:15 | 290 min | 20 min | 0 | +20 min |
| 08:00–12:00 | 08:15–12:15 | 240 min | 15 min | 15 min | 0 |
| 08:00–12:00 | 08:00:59–12:00:01 | 240 min | 0 | 0 | 0 |
| 08:00–12:00 y 13:00–17:00 | 08:00–17:00, sin confirmar pausa | No acreditar intervalo continuo | Pendiente | Pendiente | Pendiente |
| Mismos dos bloques | 08:00–17:00, pausa trabajada confirmada | 540 min | 60 min | 0 | +60 min |
| 08:00–12:00 | Solo 12:00 | 0 min confirmados; no afirma ausencia | Pendiente | Pendiente | Pendiente |
| 08:00–12:00 | No trabajó, Otro confirmado | 0 | 0 | 240 min | −240 min |
| 08:00–12:00 | Licencia/enfermedad confirmada, sin marcas | 0 | 0 | 0 | 0, justificado |

Los intervalos se comparan como conjuntos, evitando sumar dos veces una superposición. Un día con un bloque completo y otro sin resolver conserva horas del completo pero no presenta saldo definitivo. En el mes solo días resueltos aportan al saldo parcial; los pendientes se enumeran. Adicional 40 y faltante 15 → saldo +25 minutos. En egreso 30/11, ese día es elegible y desde 1/12 no genera previstos; un evento de 1/12 es incidencia excluida.

## Recorridos de interfaz

1. Abrir mes: recuperar último snapshot, solicitar actualización sin exponer secretos, mostrar carga/error independiente del estado laboral.
2. Revisar día: originales en HH:mm, horario aplicable, posiciones, faltantes y motivo opcional; completar, asignar o confirmar no trabajo/sin pausa; ver historial.
3. Horario laboral: carga inicial sugerida, edición semanal con vigencia; excepción por fecha y margen general vigente; vista previa y confirmación para efectos retroactivos.
4. Resumen: confirmadas y previstas; adicional, faltante y saldo; días por revisar y parcialidad. Licencia/enfermedad identificadas para explicar ausencia de faltante.

Respetar [sistema visual](../../ui/sistema-visual.md), foco/diálogos accesibles, errores junto al campo, éxito persistente cerrable, borrador conservado y confirmación de descarte. No llevar la barra de revisión de la maqueta al producto.

## Límites y estado de aprobación

Q1–Q31 y el cierre funcional están aprobados. La formalización matemática y el contrato propuesto deben revisarse antes de implementar. Jornadas que crucen medianoche, conflictos de datos del proveedor o combinaciones colapsadas al minuto no tienen reglas de negocio inventadas: deben rechazarse como configuración no admitida o quedar por revisar según el diseño técnico a validar. Si la implementación requiere ampliar esos comportamientos, presentar un caso concreto, sin asumirlo.
