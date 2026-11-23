# CU3 — Registro de horas por empleado

Fecha: 23/11/2026. Actor: administración. Nombre del caso de uso: registro de horas por empleado; alcance funcional aprobado inicialmente para maestras, no ampliado automáticamente a todos los roles. Discovery Q1–Q31 cerrado por Maxi. Interfaz inicial MagicPath aprobada; producto aún no implementado por estos documentos.

## Objetivo y ubicación

Ficha → Registro de horas, mes y tabla diaria, originales, intervalos confirmados, previstos, adicional, faltante, saldo neto e incidencias. Solo informativo, sin pagos, recargos, aprobación de pago o cierre mensual.

Fuente propietaria completa: [reglas funcionales Q1–Q31](../registro-horas.md). [Iniciativa 010](../../specs/010-time-records/spec.md): AC01–AC24, propuesta técnica, plan y tareas. No duplicar ni reemplazar esas reglas en nuevas sesiones; este documento delimita el caso respecto de CU1/CU2.

## Dependencias y datos externos

CU2 aporta vínculo validado y documento externo. CU3 no llama Employees para redescubrir al empleado. Consulta Bearer GET `/api/Attendance/getAttendances?document=...&start=...&end=...` sobre Portal del Empleado; lectura por fechas probada por Maxi, filtro document pendiente. Autenticación compartida con CU1/CU2 en backend.

Muestra de marca: code, external_id nulo, document, full_name, group, device, issued, created, created_by y metadata de validación. No se observó campo de dirección entrada/salida. code de asistencia no equivale al code del empleado. issued/created sin offset y estabilidad de evento deben validarse antes de normalizar/importar. Conservar original íntegro, sin exponer segundos en UI.

## Reglas consolidadas que deben preservarse

- Horario laboral propio por maestra, bloques semanales con vigencia y excepciones por fecha. Precarga inicial editable desde cursos, sin herencia posterior. Editor Horario laboral dentro de la pestaña. Plantillas externas son propuesta pendiente de CU1, no requisito de CU3.
- Margen general de KUME inicial 60 minutos con vigencia. Reproceso retroactivo de margen/horario: vista de afectados, confirmación, auditoría y preservación de originales.
- Solo interpretar automáticamente combinaciones inequívocas en orden sin reutilizar eventos; resto por revisar. Administración puede asignar originales fuera del margen, nunca modificar marcas Clock.
- Completar faltantes manualmente, siempre con motivo opcional. Una marca nueva inequívoca para ese faltante reemplaza la hora manual usada, conservando historia; varias candidatas no sobrescriben silenciosamente.
- Truncar cada marca al minuto antes del cálculo; conservar timestamp original. Comparar intervalos reales y previstos como conjuntos, no solo duración. Mostrar adicional, faltante y diferencia neta diaria/mensual, sin efectos de pago.
- Día incompleto: horas de tramos completos visibles pero saldo pendiente; mes parcial y pendientes visibles. Nunca convertir desconocido en faltante confirmado ni futuro en ausencia.
- Trabajo durante pausa requiere confirmación expresa; mantener ocho horas previstas y nueve reales si trabajó 08:00–17:00 sin pausa sobre dos bloques de ocho horas.
- Sin jornada prevista y con marcas: revisar y configurar jornada excepcional antes de calcular saldo. Antes de primera vigencia no inferir historia inexistente.
- Confirmar que no trabajó: Licencia / Enfermedad / Otro y causa opcional. Primeras dos sin faltante; Otro conserva referencia y faltante confirmado.
- Fichas inactivas: revisión histórica sin reactivar. Egreso inclusivo, sin previstos desde el día siguiente. Marcas posteriores se conservan como incidencia excluida de cálculos automáticos.
- Consulta al abrir/cambiar mes y botón Actualizar; conservar último éxito ante fallo con antigüedad visible. Sin tarea programada. Meses abiertos, auditoría y concurrencia optimista.

## Secuencia de consulta propuesta

```mermaid
sequenceDiagram
    actor A as Administración
    participant UI as Registro de horas KUME
    participant BE as Backend KUME
    participant DB as Base KUME
    participant C as API Clock
    A->>UI: Abrir maestra y mes
    UI->>BE: Leer snapshot persistido
    BE->>DB: Leer diario, configuración y último éxito
    DB-->>BE: Snapshot o primer uso
    BE-->>UI: Datos locales y estado de consulta
    UI->>BE: Solicitar actualización del mes
    BE->>DB: Leer vínculo CU2
    DB-->>BE: Vínculo/documento externo
    alt Vínculo válido
        BE->>C: GET /api/Attendance/getAttendances con documento y fechas
        C-->>BE: Respuesta
        alt Respuesta válida y cobertura comprobada
            BE->>DB: Importar y reconciliar con decisiones actuales
            Note over BE,DB: Red fuera de transacción; aplicación atómica
            DB-->>BE: Nuevo snapshot e historial
            BE-->>UI: Marcas, cálculos y último éxito
        else Error o respuesta no confiable
            BE-->>UI: Conservar último éxito y mostrar actualización fallida
        end
    else Falta vínculo o identidad requiere revisión
        BE-->>UI: Solicitar resolución en CU2, sin descubrimiento automático
    end
```

## Evidencia, límites y continuidad

MagicPath: proyecto `473074895715196928`, componente `473074931341623296`, revisión inicial aprobada `473077607060094976`. [Maqueta y capturas](../../ui/maquetas/registro-horas/README.md). La maqueta usa datos simulados y no refleja automáticamente todas las ampliaciones de Q1–Q31; no copiar su almacenamiento en memoria ni lógica predefinida al producto.

Pendientes técnicos: V01–V07 de [tareas](../../specs/010-time-records/tasks.md), identidad temporal/externa, cobertura, protocolo de renovación y errores; revisar fórmula/matching, esquema, transacciones y contrato interno antes de desarrollar. OpenAPI todavía no incluye estas rutas. Originales modificados/omitidos por proveedor no justifican pérdida de historia ni borrado por omisión.

Criterios de salida: AC01–AC24 verificables, ejemplos de cálculo correctos, lectura real por documento validada, originales inmutables, ajustes/versiones sin pérdidas bajo concurrencia, pruebas reales de PostgreSQL separadas del simulador y comportamiento de error integrado. No declarar integración real por pasar unitarias.

[Prompt de esta sesión](../../general/prompts/softwareclock/03-registro-horas.md). [Índice y dependencias](README.md).
