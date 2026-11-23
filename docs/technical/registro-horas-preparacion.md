# Registro de horas — Preparación de especificaciones y conexión

> **Continuación por caso de uso:** [CU1 horarios](../functional/softwareclock/sincronizar-horarios.md), [CU2 empleado](../functional/softwareclock/sincronizar-empleado.md), [CU3 horas](../functional/softwareclock/registro-horas.md). [Índice y prompts](../functional/softwareclock/README.md). La documentación anterior conserva evidencia y contexto; los turnos ya tienen muestra de respuesta documentada.

Fecha: 16 de noviembre de 2026. Estado: documentación de continuidad tras aprobación de reglas e interfaz por Maxi. No es una especificación técnica terminada ni evidencia de integración implementada.

## Punto de partida

Maxi aprobó el prototipo y pidió documentar todas las decisiones para comenzar las especificaciones y la conexión con la API de Clock. Conservar esos acuerdos y avanzar sobre los pendientes; no volver a preguntar por decisiones resueltas salvo contradicción concreta.

| Fuente propietaria | Contenido que debe consumirse |
| --- | --- |
| [Reglas funcionales](../functional/registro-horas.md) | Alcance, interpretación, horarios, cómputo de horas, correcciones y estados |
| [Maqueta aprobada](../ui/maquetas/registro-horas/README.md) | Identificadores MagicPath, composición, recorridos, fuentes, capturas y límites |
| [API de SoftwareClock](softwareclock-api.md) | Autenticación comprobada, URL, llamadas, ejemplo ficticio y validaciones pendientes |
| [Sistema visual](../ui/sistema-visual.md) | Paleta, tipografía, controles, estados y accesibilidad comunes |
| [Personal V1](../specs/005-staff/spec.md) | Modelo actual de ficha y asignaciones; horas era una exclusión de esa entrega |
| [OpenAPI](../../openapi.yaml), [API KUME](api-design.md) y [base](backend/database-design.md) | Contratos y persistencia actuales; todavía sin módulo de horas |
| [Arquitectura backend](backend/backend-architecture.md) y [frontend](frontend/frontend-architecture.md) | Capas, adaptadores, validación, consultas y componentes del producto |

## Decisiones cerradas que no deben reabrirse

La fuente de detalle sigue siendo el documento funcional, sin duplicar aquí sus tablas o endpoints. Para el traspaso, están resueltos: revisión de asistencia sin liquidación salarial; pantalla por maestra dentro de su ficha; horario laboral propio por maestra con vigencias, bloques semanales y excepciones por fecha (actualización Q1–Q8 del 23/11); bloques y pausas explícitos; interpretación sugerida sin inventar faltantes; margen configurable inicial de 60 minutos; revisión de ambigüedades sin descartar eventos; ajustes exclusivamente administrativos, locales a KUME, con motivo siempre opcional y auditoría; consulta al abrir/cambiar mes y actualización manual; totales separados y cómputo solo de tramos completos no ambiguos.

La aprobación visual corresponde a la revisión `473077607060094976`, componente `473074931341623296`, proyecto MagicPath `473074895715196928`. No obliga a copiar el código de demostración al frontend ni a reproducir herramientas de revisión dentro del producto.

## Entregables de la etapa de especificación

Preparar una iniciativa en `docs/specs` siguiendo la organización existente, al comenzar esa etapa. Actualización del 23/11: iniciativa [010-time-records](../specs/010-time-records/spec.md) preparada con especificación funcional, propuesta técnica, plan y tareas; esta guía queda como contexto de discovery.

1. **Especificación funcional:** historias, vocabulario de marca original, asignación de evento, ajuste, bloque y tramo confirmado; criterios de aceptación trazables a las decisiones aprobadas.
2. **Especificación técnica:** ciclo de importación, adaptador de Clock, gestión backend del token, normalización temporal/documental, persistencia, auditoría, concurrencia y cálculo de estados/horas. Presentar alternativas para los pendientes que afecten reglas de negocio.
3. **Contrato y base:** reconciliar rutas internas, DTO, errores, permisos y versionado con OpenAPI y guías canónicas; diseñar migraciones aditivas. No confundir rutas externas `/api/...` con las internas de KUME `/api/v1/...`.
4. **Plan y tareas:** separar documentación/contrato, backend, frontend, pruebas y operación. Definir dependencias, evidencia esperada y coordinación de consumidores de la revisión documental.
5. **Validación de conexión:** ejecutar las comprobaciones del proveedor con credenciales custodiadas en backend o prueba local autorizada; registrar solo resultados anonimizados. No pedir ni copiar secretos en chat, documentos o fixtures.

No agregar una dependencia de producción ni alterar un contrato público por inferencia: las aprobaciones necesarias se resuelven sobre propuestas concretas según las reglas del repositorio.

## Preguntas técnicas pendientes y evidencia que las resuelve

| Tema | Trabajo necesario antes de cerrar el diseño |
| --- | --- |
| Horarios históricos | Q1/Q4 aprobados: horarios propios con inicio de vigencia; antes de la primera referencia no inferir. Diseñar persistencia y carga histórica explícita |
| Bloques y margen | Definir dónde se configuran, quién los modifica dentro de administración y su alcance; no convertir el rango ficticio 0–180 en límite de negocio |
| Interpretación ambigua | Especificar candidatos que se solapan, igualdad de horas, eventos fuera del margen, marcas excedentes y cambios de estado; no adoptar automáticamente «el más cercano» |
| Identidad de eventos | Comprobar estabilidad y alcance de `code`; decidir clave de importación sin descartar dos eventos válidos con igual hora |
| Vínculo de maestra | Validar filtro `document`, normalización y correspondencia única con cédula KUME; nunca vincular solo por nombre |
| Tiempo del proveedor | Confirmar zona/offset, precisión y diferencia entre `issued` y `created`; no inferir UTC del formato sin zona |
| Mes consultado | Confirmar límites inclusivos, cobertura, orden y posible truncamiento; una respuesta larga no demuestra integridad |
| Token y fallos | Confirmar vencimiento, renovación, revocación y permisos; contemplar errores HTTP y errores dentro de HTTP 200 |
| Reimportación | Diseñar idempotencia y detección de eventos modificados/tardíos; preservar auditoría y ajustes locales |
| Conflicto con ajuste | Q3/Q5 aprobados: reemplazar hora manual por marca Clock únicamente con correspondencia inequívoca, auditar; ambigüedad conserva ajuste y exige revisión |
| Versionado | Definir recurso propietario de la versión y rechazo de escrituras obsoletas compatible con el control optimista vigente |
| Caché y consulta fallida | Definir unidad de caché por persona/mes, consulta concurrente, actualización atómica y antigüedad visible; preservar última consulta exitosa |

Los datos del proveedor se validan con lectura/documentación o pruebas acotadas; las decisiones que cambien comportamiento se presentan a Maxi. No convertir hechos aún no comprobados en acuerdos funcionales.

## Casos que deben cubrir las especificaciones y pruebas

- Dos bloques completos: sumar duración real de ambos sin incluir la pausa.
- Un bloque completo y otro incompleto: sumar únicamente el completo y mantener el día por revisar.
- Una sola marca al final del bloque: sugerir posible salida, mantener entrada vacía y no estimar horas.
- Dos marcas cercanas candidatas a la misma entrada: conservar ambas y exigir resolución explícita.
- Un evento candidato a salida de mañana o regreso de tarde dentro del margen: no usarlo en ambas posiciones ni resolver silenciosamente.
- Día previsto sin eventos frente a día sin jornada prevista y frente a eventos sin horario: estados distintos, sin declarar ausencia automáticamente.
- Jornada actual antes, en y después del límite de hora prevista más margen; bloques futuros pendientes.
- Ajuste sin motivo: aceptado, con autor, fecha y cambios antes/después. Motivo vacío nunca bloquea.
- Ajuste inválido: horas fuera de orden o una misma marca reutilizada; conservar borrador y explicar error.
- Actualizar el mismo período dos veces: no duplicar marcas ni perder ajustes. Evento tardío o modificado: aplicar la política acordada, conservando auditoría.
- Fallo de Clock con datos guardados: conservar última consulta, identificar antigüedad y permitir reintento; no transformar el fallo en cero horas o ausencia.
- Cambio histórico de asignación: no alterar meses anteriores usando silenciosamente la asignación actual.
- Dos administradores editando el mismo registro: conservar trabajo y rechazar escritura obsoleta sin sobrescritura.
- Credenciales/token del proveedor nunca llegan al navegador ni a logs; consultas y ajustes exigen sesión KUME.

Los últimos casos técnicos son criterios para completar el diseño, no comprobaciones ya ejecutadas. Las pruebas de la maqueta solo acreditan los recorridos documentados en su memoria.

## Secuencia de continuación

Primero especificar el comportamiento pendiente y validar el contrato real de Clock que lo condiciona. Después cerrar contrato interno y persistencia, preparar plan y tareas y desarrollar el adaptador backend y la interfaz sobre los componentes existentes. Verificar integración y despliegue como hitos separados.

El acceso básico a Clock ya fue validado manualmente por Maxi: no reiniciar la búsqueda de API key. El mecanismo comprobado es usuario API con Basic para obtener token y Bearer para consultar asistencias, en Portal del Empleado. Las próximas pruebas se enfocan en lo todavía desconocido.

Estado al entregar esta documentación: reglas e interfaz aprobadas, conectividad básica comprobada por el usuario, fuentes documentales reconciliadas; especificaciones completas, contrato interno, persistencia e integración del producto pendientes. No se marca completo el paso 4 general ni se ejecutan migraciones o despliegues por documentar esta aprobación. Maxi autorizó posteriormente commit y push de la documentación.

## Discovery retomado — 23 de noviembre de 2026

Q1–Q31 resueltos en conversación: las actualizaciones y ejemplos pertenecen a [reglas funcionales](../functional/registro-horas.md). Cambios principales frente al prototipo inicial: horario laboral propio con vigencias y excepciones; reemplazo automático acotado de hora manual por marca real; comparación informativa de tiempo adicional/faltante con saldo neto y parcialidad. La composición inicial sigue aprobada, pero estas ampliaciones requieren adaptación y revisión; no se modificó MagicPath ni se implementaron contratos por registrarlas.

Q13–Q17 resuelven trabajo en fechas sin jornada, truncamiento al minuto y agregación por intervalos con saldo mensual neto. Q18/Q19 exigen confirmación de trabajo sin pausa conservando la referencia prevista y registrando los intervalos reales por separado. Siguen pendientes el diseño técnico de editores/configuración, el algoritmo conforme la regla inequívoca aprobada y las validaciones del proveedor. No cerrar las especificaciones mientras estos puntos estén sin resolver.

Q20/Q21 fijan editor en Registro de horas y herencia de cursos exclusivamente para precarga inicial. Q22/Q25 definen confirmación de no trabajo y clasificación con causa opcional: licencia/enfermedad sin faltante, Otro con faltante confirmado. Q23 prohíbe modificar marcas Clock; Q24 mantiene meses abiertos; Q26 exige interpretación única o revisión. Detalle en la fuente funcional. Q27/Q28 resuelven margen general con vigencias y reproceso retroactivo confirmado; pendientes comprobaciones del proveedor; reglas aprobadas no acreditan contratos ni implementación.

## Balance tras Q31

Q27–Q31: margen global con vigencias; revisión de jornadas de maestras inactivas sin reactivación; egreso inclusivo; eventos posteriores al egreso conservados para revisión y excluidos de cálculos automáticos. Detalle propietario en reglas funcionales.

Maxi confirmó expresamente el cierre del discovery funcional después de Q31. No dar por realizadas las validaciones técnicas pendientes. La siguiente etapa prepara especificación funcional, especificación técnica, plan y tareas, y diseña contratos internos y persistencia. La validación de Clock sigue abierta: filtro por documento, zona horaria, identidad estable de eventos, límites/cobertura de consulta, expiración/renovación y errores. Son hechos a investigar y probar, no decisiones a resolver por recomendaciones al usuario.

## Continuación activa tras confirmación de Maxi

Discovery funcional cerrado el 23/11/2026. Continuar desde [spec](../specs/010-time-records/spec.md), [diseño técnico propuesto](../specs/010-time-records/technical-spec.md), [plan](../specs/010-time-records/plan.md) y [tareas](../specs/010-time-records/tasks.md). Primero revisar propuesta contractual y validar Clock; las menciones anteriores a especificaciones aún sin crear son el estado histórico previo a esta entrega. No se implementó ni ejecutó una conexión real por preparar la documentación.
