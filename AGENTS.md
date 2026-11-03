# Instrucciones para agentes — kume-admin-docs

## Antes de trabajar

Leer implementation-decisions.md, alcance-prototipo.md y stack-tecnologico.md. Para contratos leer api-design.md y openapi.yaml; para persistencia database-design.md; para UX continuacion-diseno-pantallas.md; para operación infraestructura-y-migracion.md. Consultar frontend-architecture.md, backend-architecture.md y development-guide.md según la tarea.

Este repositorio define alcance, contratos y pautas de implementación. Trabajar directamente sobre main, conservando cambios ajenos. Si el checkout usa otra rama, comprobar su estado y referencias antes de cambiar; no forzar ni descartar trabajo para cumplir la convención.

## Fuentes de verdad

- Alcance funcional: alcance-prototipo.md más decisiones posteriores explícitamente aprobadas y registradas.
- Stack: stack-tecnologico.md y ampliaciones de implementation-decisions.md.
- HTTP: openapi.yaml; api-design.md explica comportamiento. Una discrepancia exige reconciliación explícita, no elegir silenciosamente una versión.
- Persistencia: database-design.md; arquitectura: las dos guías correspondientes.
- Estado de pantallas: continuacion-diseno-pantallas.md. No marcar el paso 4 completo sin confirmación expresa de Maxi.

Las nuevas decisiones de arquitectura complementan el diseño funcional. La estrategia optimista está aprobada pero sus campos, cabeceras y migraciones todavía no figuran en el contrato original. Sesiones siguen pendientes. No confundir decisión con implementación.

## Al editar

Actualizar la fuente propietaria de cada regla y enlazarla desde otros documentos. No duplicar listados de campos, endpoints ni reglas de negocio en AGENTS. Mantener español en documentación y textos visibles; vocabulario técnico del código en inglés.

Para cambios funcionales reconciliar alcance, API/OpenAPI y base según corresponda. Registrar motivo, estado, impacto entre repositorios y pendientes. Diferenciar propuesta, aprobado, implementado y verificado. No completar pantallas ni backlog por inferencia.

No guardar secretos, datos reales ni archivos privados. Ejemplos y fixtures deben ser ficticios. Conservar archivos de referencia y aprobaciones existentes.

## Verificación y entrega

Comprobar enlaces relativos, Markdown, coherencia de decisiones y, si cambia OpenAPI, validación y compatibilidad del contrato. Describir verificaciones realizadas y límites. No inventar scripts ni afirmar que se ejecutaron controles inexistentes.

Consultar antes de cambiar stack, incorporar dependencias de producción no acordadas, alterar contratos públicos o permisos, o ejecutar cambios destructivos en datos. Los detalles internos y correcciones dentro de las reglas aprobadas son autónomos. No hacer commit ni push salvo pedido explícito. La autorización expresa de la sesión prevalece y no se pide nuevamente.
