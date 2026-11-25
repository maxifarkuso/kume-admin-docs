# CU2 — Plan de implementación y pruebas

| Etapa | Entrega y condición de salida |
| --- | --- |
| 1. Validar lecturas | Con CU0, comprobar alcance, respuesta por cédula y estabilidad del ID. Con CU1, verificar que la asignación pueda resolverse con garantías suficientes. Usar lecturas autorizadas y conservar evidencia resumida y anonimizada. |
| 2. Acordar contrato | Revisar estados UX, política de acceso y revalidación, códigos, retención, versiones y constraints con Maxi. Reconciliar OpenAPI, diseño de base y revisiones fijadas por FE/BE después de aprobación. La definición estructurada de CU1 y el modelo de horario propio de 010 condicionan la entrega de la propuesta inicial. |
| 3. Implementar por hitos | Backend primero con vista previa, confirmación y vínculo; entregar estados pendientes aunque falte definición estructurada. Agregar la copia inicial cuando existan ambos modelos. Frontend incorpora acción y estados en Personal con DTO generados. CU3 acuerda el puerto de lectura y la revisión usada por importación. |
| 4. Verificar | Controles existentes de contrato y CI, pruebas unitarias y comportamiento FE, y pruebas de base/transacción en entorno aprobado. Lecturas reales de Clock solo con autorización y sin datos reales en evidencia de prueba. Operación y despliegue requieren autorización propia. |

La [decisión de alcance aprobada](../../general/implementation-decisions.md#cu2--alcance-y-habilitación-acordados-con-maxi) separa vínculo y horario en dos hitos. Ambos conservan sus criterios de aceptación.

## Matriz de pruebas pendientes

| Aceptación | Nivel y casos |
| --- | --- |
| CU2-01–02 | Backend unitario y fixtures ficticios: formatos, ceros, documento discrepante, ausencia, ID no apto y respuestas inválidas. |
| CU2-03–05 | Dominio y UI: edición de un bloque y pausa, vigencia retroactiva con confirmación, solapes, cancelar, guardar solo identidad, turno ausente o duplicado, códigos vacíos, par local insuficiente y reintento explícito tras configurar. |
| CU2-06–07 | Backend y base: cambio de turno/CU1 sin escritura al horario, cédula cambiada, identidad usada por otra ficha, conservar revisiones de origen e importaciones históricas. |
| CU2-08 | Base: dos confirmaciones concurrentes, cambio de ficha, catálogo o horario entre vista y guardado, rollback tras error al auditar, reenvío idéntico y distinto. UI: borrador, sesión, timeout y conflicto sin sobrescritura. |
| CU2-09 | Autorización y contrato: ficha inactiva, vista ajena o vencida, CSRF según guardas vigentes, ausencia de documentos/credenciales en logs. CU3: revisión congelada, cambio durante importación y verificación real de filtro por documento. |

## Estado del 24/11/2026

- **Aprobado por Maxi:** dos hitos, alcance del vínculo y las tres operaciones HTTP del primero, empresa determinada por el token de CU0, confirmación real condicionada a evidencia, revalidación de la misma identidad y vista previa de 15 minutos.
- **Implementado localmente en el primer hito:** OpenAPI, acción de ficha, confirmación y persistencia versionada con auditoría, revalidación, y conservación de la referencia de Clock. El flujo muestra el horario pendiente. FE consume tipos generados del subconjunto CU2 mientras se publica y fija la nueva revisión documental.
- **Verificado con datos ficticios:** cobertura unitaria de FE/BE y prueba local de HTTP y Prisma con migraciones sobre PGlite. La prueba de base cubre confirmación, repetición, revalidación, suspensión y rollback ante una identidad ya vinculada. Quedan por verificar concurrencia sobre PostgreSQL y el perfil real de la API.
- **Pendiente:** habilitación operativa en Oracle con la estabilidad del ID externo como supuesto aprobado. La definición estructurada de CU1 y el horario editable corresponden al segundo hito. CU3 mantiene pendiente validar la lectura por documento de asistencias.
