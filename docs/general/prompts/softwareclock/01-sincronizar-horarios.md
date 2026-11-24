# Prompt 1 — Sincronizar workshifts / horarios laborales

Continuemos KUME Admin, exclusivamente con el caso de uso «Sincronizar workshifts / horarios laborales».

Repositorio documental: maxifarkuso/kume-admin-docs. Frontend: maxifarkuso/kume-admin-fe. Backend: maxifarkuso/kume-admin-be. Inspeccioná el estado actual y AGENTS.md de cada checkout antes de trabajar; preservá cambios de otras sesiones.

Leé primero:
- docs/functional/softwareclock/README.md
- docs/functional/softwareclock/sincronizar-horarios.md
- docs/technical/softwareclock-api.md
- docs/technical/softwareclock-employee-mapping.md
- docs/general/implementation-decisions.md y docs/ui/sistema-visual.md
- Para contratos/persistencia: openapi.yaml, docs/technical/api-design.md y docs/technical/backend/database-design.md.

Contexto comprobado por muestras aportadas por Maxi: la base es https://api.portalempleado.softwareclock.com/. GET /api/ClockApiUser usa Basic con usuario API y devuelve token; las lecturas posteriores usan Bearer. GET /api/EmployeesWorkShifts/getWorkShifts devuelve un array de code, name y type. Hay turnos Fijo/Libre y varios códigos vacíos para nombres distintos. La respuesta no tiene días, bloques, pausas ni vigencias estructuradas; no extraigas reglas horarias del nombre ni interpretes Libre como 24 horas de trabajo.

Maxi pidió Administración → Horarios laborales → Importar desde Clock. Diseñá lectura, vista previa, confirmación, identidad local, correspondencias, reimportación, conflictos y estados. No uses code vacío, nombre o posición del array como clave estable. Conservá definiciones locales y auditoría al actualizar; ninguna reimportación debe modificar horarios de maestras.

Investigá si existe detalle estructurado adicional y verificá alcance/estabilidad de códigos; no inventes endpoints o parámetros ni des por realizadas pruebas autenticadas. Si necesitás evidencia del usuario, pedí solo muestra anonimizada o ejecución local segura, nunca tokens en chat. La configuración local de días/bloques/pausas y su uso como plantillas seleccionables son propuestas pendientes de confirmar; CU2 requiere la definición estructurada del workshift para proponer una copia inicial editable e independiente.

Documentá secuencias con Mermaid. Prepará/reconciliá especificación, propuesta técnica, criterios de aceptación, plan y tareas propios de CU1. Cerrá únicamente decisiones nuevas sobre propuestas concretas; no reabras Q1–Q31 del registro de horas. Reutilizá el conector/autenticación backend existente si existe, sin crear otro por sesión. No implementes CU2/CU3 ni escribas en Clock. Antes de alterar contrato público/stack/dependencias cumplí las aprobaciones de AGENTS. Diferenciá aprobado, propuesto, implementado y verificado; no presupongas autorización de commit/push, merge, producción o despliegue por este prompt.
