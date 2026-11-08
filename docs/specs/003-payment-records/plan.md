# Registro de pagos — plan de implementación

Fecha: 8 de noviembre de 2026. Implementación solicitada por Maxi; estado verificable en [tareas](tasks.md).

| Orden | Hito                    | Condición de salida                                                                                                    |
| ----- | ----------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| 1     | Especificación técnica  | Límites, dinero/fechas, archivos, persistencia y UX trazados a AC1–AC16.                                               |
| 2     | Resolver bloqueos       | Decisiones aprobadas: versionado, America/Montevideo y @fastify/multipart; documentar impacto contractual.             |
| 3     | Preparar consumidores   | Revisar instrucciones y referencias; ramas feature; contrato inmutable y DTO generados si corresponde.                 |
| 4     | Rubros y núcleo         | Catálogo necesario y carga inicial; importes exactos, fechas civiles, invariantes y unitarias.                         |
| 5     | Persistencia y archivos | Migraciones revisadas, puertos/adaptadores y compensaciones; coordinación transaccional de rubros y gastos.            |
| 6     | HTTP                    | Registrar operaciones canónicas con autenticación, protección de escritura, validación, errores, filtros, total y CSV. |
| 7     | Frontend                | Listado, filtros, total, formularios, detalle, comprobantes y estados; mantener borradores y contexto.                 |
| 8     | Verificación            | Controles de ambos repositorios y revisión del diff; evidencia diferenciada de límites de integración.                 |
| 9     | Entrega                 | Registrar archivos, comandos y pendientes; publicación y operación requieren su autorización correspondiente.          |

No ejecutar migraciones hasta la etapa previa al despliegue, según la instrucción conservada del proyecto. No mezclar esta feature con limpieza general ni actualizar dependencias ajenas.

## Trazabilidad de verificación

- AC1, AC11–AC13: filtros, URL, paginación, consistencia de total, CSV completo y exactitud decimal.
- AC2–AC5: validaciones, fecha límite, carga válida/rechazada, compensación y conservación del formulario.
- AC6–AC10, AC14: detalle, archivos privados, transición de estados, reemplazo fallido y rubro inactivo.
- AC15–AC16: errores públicos seguros, sesión y no reenvío automático de escrituras.
- Concurrencia: añadir casos específicos solo con el protocolo aprobado; distinguir tests con dobles de carreras reales.
