# Implementación y evidencia — cursos y talleres

Fecha: 7 de noviembre de 2026. Rama de código: feat/courses-workshops. Implementación local completada; verificación de producción y migraciones pendientes.

## Resultado

Backend con módulo catalogs, dominio independiente, casos de uso/puerto, adaptador Prisma, doce operaciones HTTP protegidas y control de versión. Tablas course/workshop, restricciones e índices únicos normalizados, timestamps y dos migraciones: schema y carga inicial de siete cursos/tres talleres. Bloqueo de fila y comparación de versión dentro de la transacción. La guarda SQL de asignaciones es consultada antes de actualizar y reforzada mediante triggers; no existe todavía una integración real con el módulo de asignaciones.

Frontend con rutas /cursos y /talleres, listados paginados, filtro de estado, búsqueda de cursos, creación, edición, confirmación de baja y reactivación. Actualizar el listado no sustituye el borrador ni su versión. Tras conflicto se puede cancelar, actualizar y reabrir conscientemente. Usa el cliente autenticado existente; no hay carga inicial en el navegador.

Contrato y guías fijados a kume-admin-docs 1e650636705371f09be51a8c77a67f39e5251ba3. El snapshot conserva la organización documental y sus recursos enlazados. Sin pendingContract ni tipos editados manualmente.

## Evidencia ejecutada

| Área     | Comprobación                                   | Resultado                                                                                                     |
| -------- | ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Backend  | format:check                                   | Correcto.                                                                                                     |
| Backend  | typecheck y lint con límites de dependencias   | Correctos con cliente Prisma local generado sin motor.                                                        |
| Backend  | test:unit                                      | 49 pruebas, 8 archivos, correctas. Incluyen dominio/aplicación y adaptador HTTP con puerto controlado.        |
| Backend  | contract:check                                 | OpenAPI, hashes, DTO y correspondencia de doce operaciones: métodos, cuerpos, estados y parámetros. Correcto. |
| Backend  | Compilación TypeScript con tsconfig.build.json | Correcta usando el cliente local sin motor. No sustituye npm run build completo.                              |
| Backend  | Schema Prisma                                  | getDMMF WASM oficial 6.19.0 analiza Course/Workshop y permite generar tipos.                                  |
| Frontend | format:check, typecheck y lint                 | Correctos.                                                                                                    |
| Frontend | test:unit                                      | 14 pruebas, 4 archivos, correctas.                                                                            |
| Frontend | build                                          | Correcto: TypeScript y Vite.                                                                                  |
| Frontend | contract:check                                 | Snapshot y generación determinista correctos.                                                                 |

## Cobertura de aceptación

AC1–AC2: adaptación HTTP de paginación/búsqueda, estado de carga/vacío/error/reintento y filtro de UI. AC3–AC4: invariantes de dominio, validación de formulario, PATCH con null y campos omitidos, respuesta 201/Location. AC5–AC7: acciones de estado probadas con puerto controlado, confirmación UI, propagación de bloqueo; restricciones SQL revisadas, pendientes de base real. AC8–AC9: escritura obsoleta y reactivación con versión, conservación de borrador/versión aun si se refresca listado. AC10–AC11: migraciones revisadas contra tablas documentadas; instalación y segunda ejecución pendientes. AC12: auth/CSRF existente, acceso sin sesión y escritura sin protección rechazados; limpieza de datos privados cubierta por App.

## Límites y paso previo al despliegue

- Riesgo alto: persistencia y concurrencia. No se ejecutaron migraciones ni pruebas PostgreSQL por pedido de Maxi; no se acredita integridad o carreras reales mediante dobles.
- npm run build del backend intenta generar el cliente con motor nativo y recibe 403 de binaries.prisma.sh en esta instancia. El dominio está agregado en la configuración mostrada por Maxi; la política activa observada todavía no lo incorpora. No se desactivaron TLS ni checksums ni se modificó el stack.
- El cliente sin motor y los archivos compilados locales no son entregables de producción. Regenerar normalmente y ejecutar npm run build completo en un entorno con acceso permitido antes de desplegar.
- Antes del despliegue ejecutar npm ci, generación nativa, controles, respaldo y npm run db:migrate sobre el destino verificado. Comprobar carga inicial y que una segunda ejecución preserve ediciones. Verificar proxy con cuerpo DELETE y comportamiento real de versión. Las migraciones no se ejecutan al arrancar API.
- CI remoto, publicación, merge y despliegue no se acreditan por commits locales. Sin datos reales ni cambios de permisos.
- Reversión sin borrar datos: regresar al artefacto anterior y conservar tablas. No hay down destructivo ni reset. La integración de asignaciones requiere el bloqueo documentado en su futura implementación.

## Commits locales de implementación

- Backend: `1c477d2`, rama `feat/courses-workshops`.
- Frontend: `e40b0d4`, rama `feat/courses-workshops`.
- Contrato y documentación consumidos por ambos: `1e650636705371f09be51a8c77a67f39e5251ba3`.

Este registro posterior no modifica el contrato fijado. Sin push, PR, merge ni despliegue en esta sesión. Las migraciones quedan preparadas y sin ejecutar por instrucción expresa de Maxi.
