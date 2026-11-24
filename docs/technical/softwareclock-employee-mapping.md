# SoftwareClock — Vinculación de empleados y resolución de turnos

[Campos y evidencia de Clock](softwareclock-api.md#respuesta-de-empleados--23112026) · [Contrato y persistencia propuestos](../specs/013-softwareclock-employee/technical-spec.md).

## Vinculación inicial y resolución

```mermaid
sequenceDiagram
    actor A as Administración
    participant UI as Ficha de Personal
    participant BE as CU2
    participant C as Conector CU0
    participant P as Clock
    participant W as Catálogo CU1
    A->>UI: Sincronizar empleado con Clock
    UI->>BE: Preparar con versión de ficha
    BE->>C: Consultar empleados
    C->>P: GET /api/Employees/employees
    P-->>C: Respuesta
    C-->>BE: Listado
    BE->>BE: Validar cobertura, documento e identidad
    alt Coincidencia única apta
        BE->>W: Resolver el turno en la misma conexión
        W-->>BE: Referencia y definición versionada o motivo pendiente
        BE-->>UI: Vista previa de identidad y resultado de horario
    else Coincidencia no comprobable
        BE-->>UI: Requiere revisión
    end
```

## Referencia inexistente, ambigua o sin configuración

```mermaid
sequenceDiagram
    actor A as Administración
    participant UI as Ficha de Personal
    participant BE as CU2
    participant DB as Base KUME
    BE-->>UI: Horario pendiente de configurar/vincular
    UI-->>A: Mostrar motivo y acceso a Horarios laborales
    A->>UI: Confirmar solo identidad
    UI->>BE: Confirmar vista previa
    BE->>DB: Guardar vínculo, referencia externa y auditoría
    BE-->>UI: Identidad vinculada y horario pendiente
    Note over A,UI: Tras resolver en CU1, preparar explícitamente otra vista
```

## Confirmación del horario inicial editable

```mermaid
sequenceDiagram
    actor A as Administración
    participant UI as Ficha de Personal
    participant BE as CU2
    participant DB as Base KUME
    BE-->>UI: Días, bloques, pausas y origen de la propuesta
    A->>UI: Editar, indicar vigencia y confirmar identidad y horario
    UI->>BE: Enviar decisión y borrador
    BE->>DB: Comprobar versiones y ausencia de horario
    alt Vista vigente y borrador válido
        BE->>DB: Guardar vínculo, copia personal, origen, auditoría y recibo
        BE-->>UI: Identidad y horario guardados
    else Conflicto o borrador inválido
        BE-->>UI: Mostrar error y conservar borrador
    end
```

## Resincro con horario propio

```mermaid
sequenceDiagram
    actor A as Administración
    participant UI as Ficha de Personal
    participant BE as CU2
    participant C as Conector CU0
    participant DB as Base KUME
    A->>UI: Sincronizar empleado con Clock
    UI->>BE: Preparar
    BE->>C: Consultar empleados
    C-->>BE: Listado
    BE->>DB: Leer vínculo y horario propio
    alt Identidad y documento siguen aptos
        BE-->>UI: Metadata externa revisable, sin propuesta de horario
        A->>UI: Confirmar actualización
        UI->>BE: Confirmar vista previa
        BE->>DB: Actualizar metadata, versiones y auditoría
        BE-->>UI: Turno actual y origen histórico diferenciados
    else Discrepancia de documento o identidad
        BE-->>UI: Solicitar revalidación y preservar historial
    end
```
