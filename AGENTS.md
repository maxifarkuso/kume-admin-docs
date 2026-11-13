# Instrucciones para agentes — kume-admin-docs

## Antes de trabajar

Leer [implementation-decisions.md](docs/general/implementation-decisions.md), [alcance-prototipo.md](docs/functional/alcance-prototipo.md) y [stack-tecnologico.md](docs/technical/stack-tecnologico.md). Para contratos leer [api-design.md](docs/technical/api-design.md) y [openapi.yaml](openapi.yaml); para persistencia [database-design.md](docs/technical/backend/database-design.md); para UX [continuacion-diseno-pantallas.md](docs/ui/continuacion-diseno-pantallas.md); para operación [infraestructura-y-migracion.md](docs/devops/infraestructura-y-migracion.md). Consultar [frontend-architecture.md](docs/technical/frontend/frontend-architecture.md), [backend-architecture.md](docs/technical/backend/backend-architecture.md) y [development-guide.md](docs/technical/development-guide.md) según la tarea.

Este repositorio define alcance, contratos y pautas de implementación. Trabajar directamente sobre main, conservando cambios ajenos. Si el checkout usa otra rama, comprobar su estado y referencias antes de cambiar; no forzar ni descartar trabajo para cumplir la convención.

## Fuentes de verdad

- Alcance funcional: [alcance-prototipo.md](docs/functional/alcance-prototipo.md) más decisiones posteriores explícitamente aprobadas y registradas.
- Stack: [stack-tecnologico.md](docs/technical/stack-tecnologico.md) y ampliaciones de [implementation-decisions.md](docs/general/implementation-decisions.md).
- HTTP: [openapi.yaml](openapi.yaml); [api-design.md](docs/technical/api-design.md) explica comportamiento. Una discrepancia exige reconciliación explícita, no elegir silenciosamente una versión.
- Persistencia: [database-design.md](docs/technical/backend/database-design.md); arquitectura: las dos guías correspondientes.
- Interfaz del sistema: [sistema-visual.md](docs/ui/sistema-visual.md), reglas generales aprobadas y referencia del piloto de Gastos; aplicar en pantallas actuales y futuras sin alterar reglas funcionales.
- Estado de pantallas: [continuacion-diseno-pantallas.md](docs/ui/continuacion-diseno-pantallas.md). No marcar el paso 4 completo sin confirmación expresa de Maxi.

Las nuevas decisiones de arquitectura complementan el diseño funcional. La estrategia optimista está aprobada pero sus campos, cabeceras y migraciones todavía no figuran en el contrato original. El diseño de sesiones está definido en [autenticacion-prototipo.md](docs/technical/autenticacion-prototipo.md). Auth foundation está mergeado y desplegado en frontend y backend según Maxi (5 de noviembre de 2026); las pruebas funcionales siguen pendientes. No confundir decisión con implementación.

## Organización documental

Consultar el [índice del repositorio](README.md) para ubicar documentos. Clasificar por responsabilidad: funcional en `docs/functional`, acuerdos generales en `docs/general`, diseño compartido en `docs/technical`, guías específicas en `docs/technical/backend` y `docs/technical/frontend`, pantallas en `docs/ui` y operación en `docs/devops`. Conservar `docs/specs` como historial de especificaciones. Al mover archivos, actualizar enlaces entrantes y salientes, referencias en skills y rutas de consumidores; las rutas documentales se expresan desde la raíz salvo enlaces relativos.

## Al editar

Actualizar la fuente propietaria de cada regla y enlazarla desde otros documentos. No duplicar listados de campos, endpoints ni reglas de negocio en AGENTS. Mantener español en documentación y textos visibles; vocabulario técnico del código en inglés.

Para cambios funcionales reconciliar alcance, API/OpenAPI y base según corresponda. Registrar motivo, estado, impacto entre repositorios y pendientes. Diferenciar propuesta, aprobado, implementado y verificado. No completar pantallas ni backlog por inferencia.

No guardar secretos, datos reales ni archivos privados. Ejemplos y fixtures deben ser ficticios. Conservar archivos de referencia y aprobaciones existentes.

## Administración y migraciones

La utilidad kume-admin conserva sus consultas y amplía su alcance por autorización
expresa del 7 de noviembre de 2026. Para desarrollarla u operarla leer la
[skill local](.agents/skills/kume-admin/SKILL.md),
[administración](docs/devops/administracion-oracle.md) y
[migraciones controladas](docs/devops/migraciones-admin.md).
Desarrollo/pruebas locales no autorizan ejecución en Oracle, instalación o despliegue.
Las reglas y límites operativos pertenecen a esas guías; conservar sus evidencias.

## Verificación y entrega

Comprobar enlaces relativos, Markdown, coherencia de decisiones y, si cambia OpenAPI, validación y compatibilidad del contrato. Describir verificaciones realizadas y límites. No inventar scripts ni afirmar que se ejecutaron controles inexistentes.

Consultar antes de cambiar stack, incorporar dependencias de producción no acordadas, alterar contratos públicos o permisos, o ejecutar cambios destructivos en datos. Los detalles internos y correcciones dentro de las reglas aprobadas son autónomos. No hacer commit ni push salvo pedido explícito. La autorización expresa de la sesión prevalece y no se pide nuevamente.
