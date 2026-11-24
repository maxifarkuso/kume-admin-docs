# CU1 — Plan

La primera entrega propuesta cubre el listado local y la importación manual de referencias descriptivas para la conexión de Clock comprobada por Maxi. La lectura usa GET sin parámetros, Bearer y el formato real documentado. La comparación por contenido y la revisión explícita permiten avanzar con códigos vacíos y sin garantías de estabilidad o cobertura del catálogo.

1. Revisar con Maxi la pantalla, las operaciones HTTP propuestas y el modelo de persistencia. Tras aprobación, reconciliar OpenAPI, API y base y fijar la referencia documental en FE/BE.
2. Integrar la lectura con CU0 y construir vista previa y confirmación en backend. Validar concurrencia, auditoría e idempotencia usando el [escenario de verificación](tasks.md#escenario-de-verificación) y pruebas con base aislada.
3. Integrar navegación, listado, vista previa y estados en frontend. Verificar el flujo desde Administración con fixtures. Después, en un entorno autorizado, probar el GET ya comprobado y verificar que la confirmación solo escribe en el catálogo de KUME.
4. Registrar evidencia y preparar la entrega. Las migraciones operativas, publicación y despliegue requieren sus autorizaciones vigentes.

La investigación de detalle estructurado, cobertura e identidad externa puede continuar en paralelo. Revisar el par local de inicio y fin, su edición y el aporte del catálogo a la definición estructurada requerida por CU2. El flujo de importación de fichas se especifica en su entrega propia.

[Especificación](spec.md) · [Propuesta técnica](technical-spec.md) · [Tareas](tasks.md)
