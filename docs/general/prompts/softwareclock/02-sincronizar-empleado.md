# Prompt 2 — Sincronizar empleado con Clock

Continuemos KUME Admin, exclusivamente con el caso de uso «Sincronizar empleado con Clock».

Repositorios: maxifarkuso/kume-admin-docs, maxifarkuso/kume-admin-fe y maxifarkuso/kume-admin-be. Inspeccioná estado y AGENTS.md de cada checkout; preservá trabajo de otras sesiones.

Leé primero:
- docs/functional/softwareclock/README.md
- docs/functional/softwareclock/sincronizar-empleado.md
- docs/technical/softwareclock-employee-mapping.md y docs/technical/softwareclock-api.md
- docs/specs/005-staff/spec.md y technical-spec.md, más ampliaciones posteriores vigentes de personal
- docs/general/implementation-decisions.md, docs/ui/sistema-visual.md, openapi.yaml y guías de API/base/arquitectura pertinentes.

UX solicitada por Maxi: botón «Sincronizar empleado con Clock» en la ficha. Objetivo: persistir el vínculo de identidad para consultar marcas posteriormente sin redescubrir al empleado cada mes.

Base comprobada https://api.portalempleado.softwareclock.com/. GET /api/ClockApiUser con Basic obtiene token; GET /api/Employees/employees usa Bearer. Maxi aportó un empleado anonimizado con id, code, document, firstName, lastName, workshiftCode, workShiftName y external_id nulo. id/code son candidatos de identidad externa, no está validado su alcance/estabilidad. code de empleado no equivale al de asistencia. document debe permanecer texto. El objeto individual no prueba cobertura ni ausencia de paginación.

Diseñá comparación por cédula/documento normalizados conservando el valor externo exacto, propuesta única y confirmación administrativa; sin coincidencia/duplicados/identidad discrepante → revisión. Nunca vincular por nombre, crear fichas automáticamente o sobrescribir datos personales/roles/horario KUME. Guardar vínculo por conexión/empresa, identidad externa, documento de consulta, versión y auditoría. Revalidar cambios de documento sin reasignar historia silenciosamente. Resincro no significa revinculación automática.

CU1 no es requisito: workshift puede conservarse como referencia informativa. CU3 consumirá el vínculo y document para GET /api/Attendance/getAttendances; no asumas filtro por id ni des por probado document. Revisá estructura/cobertura de Employees y estabilidad de identidad antes de cerrar constraints. GET /api/Employees/employee-by-rut es una alternativa documentada no probada; evaluarla no reemplaza silenciosamente el listado solicitado.

Documentá secuencias Mermaid y entregá especificación, propuesta de contrato/persistencia/versiones, estados UX, casos de concurrencia, plan y tareas. Buscá/reutilizá conector compartido si ya existe. Usá datos ficticios y evidencias anonimizadas; credenciales/token solo backend. No implementes catálogo CU1 ni cálculo CU3, ni escribas en Clock. Cumplí aprobaciones de AGENTS antes de alterar contrato público/stack/dependencias. Diferenciá evidencia del usuario de pruebas propias; este prompt no presupone commit/push, merge, migración productiva ni despliegue.
