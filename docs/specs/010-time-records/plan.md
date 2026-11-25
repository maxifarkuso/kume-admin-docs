# Registro de horas — Plan de implementación

Fecha: 23 de noviembre de 2026. Plan propuesto tras cierre funcional; no acredita implementación. Ver [especificación](spec.md), [diseño técnico](technical-spec.md) y [tareas](tasks.md).

| Orden | Hito | Condición de salida |
| --- | --- | --- |
| 1 | Cierre funcional y documentación | Q1–Q31 registrados, AC01–AC28 y ejemplos revisables; cierre confirmado por Maxi |
| 2 | Validar endpoints, vinculación y proveedor | Resolver matriz V01–V07 de tareas o documentar con precisión qué bloquea al adaptador; sin secretos en evidencias |
| 3 | Revisar propuesta técnica y contrato | Recursos/versiones, matching, snapshots, esquema y errores concretos revisados; autorización del contrato local registrada el 25/11; revisar matching y esquema antes de persistir |
| 4 | Preparar consumidores | Contrato canónico ampliado localmente y validado, revisión inmutable publicada cuando se autorice, FE/BE fijados a la misma revisión y DTO generados |
| 5 | Núcleo y configuración | Horarios propios precargados una vez, vigencias, excepciones, margen y previsualización/reproceso; dominio probado con ejemplos |
| 6 | Persistencia y auditoría | Migración aditiva revisada, idempotencia y revisiones originales; transacciones/versionado comprobados en base de prueba |
| 7 | Adaptador y casos de uso | Lectura Clock, autenticación backend, importación atómica, preservación de ajustes y fallos que conservan snapshot |
| 8 | API KUME | Rutas canónicas, sesión, protección de comandos, validación/error y pruebas de contrato sin escribir en Clock |
| 9 | Frontend | Adaptar interfaz aprobada con horarios, excepciones, saldos y revisión; originales inmutables, borradores y accesibilidad |
| 10 | Verificación integrada | Pruebas FE/BE, contrato, base y carreras; recorrido real de lectura autorizado, anonimizado y separado del simulador |
| 11 | Preparar entrega | Evidencia de commits/PR y comprobaciones, revisión del diseño ampliado; no merge/migración productiva ni despliegue implícitos |

El núcleo y fixtures de dominio pueden prepararse mientras se valida el proveedor; no fijar identidad temporal/externa del adaptador sin evidencia. Validación de filtro/cobertura precede la importación real. La escritura HTTP depende del contrato aprobado, y las carreras reales dependen de base de prueba.

## Impacto entre repositorios

- Docs: fuente funcional, iniciativa, API/base y OpenAPI coordinados cuando se apruebe el contrato.
- Backend: nuevo módulo y migración; coordinación con Personal para identidad/egreso; configuración privada de Clock y cliente de red acotado.
- Frontend: habilitar pestaña para el alcance aprobado al disponer del backend; nuevos formularios, totales y estados, sin reproducir código simulado.
- Operación: secrets backend, conectividad desde Oracle o intranet, respaldo de nuevas tablas y ensayo de recuperación; no exige contratar servicio ni cambiar stack.

Conservar cambios ajenos, ramas y revisión según instrucciones de cada repo. No ejecutar migraciones de producción durante desarrollo. La indisponibilidad de Clock no debe impedir consultar registros ya importados ni el resto de KUME.

## Trazabilidad de verificación

- AC02–AC06: horarios/vigencias/precarga única/excepciones y confirmación retroactiva.
- AC07–AC11: candidatos, emparejamiento único, reemplazo de faltante y originales inmutables.
- AC12–AC19: estados temporales, cálculo con minutos, parciales, pausas y justificaciones.
- AC25–AC28: acceso por vínculo, habilitación sin recarga, horario pendiente y revalidación con historial.
- AC20–AC24: egreso inclusivo, inactivas, consulta/error, seguridad y carreras reales.

La autorización de preparar estas especificaciones no prueba ni publica un contrato nuevo. Resolver la revisión técnica sobre los archivos concretos, sin repetir discovery funcional.

Prioridad indicada por Maxi el 23/11: cerrar primero [vínculo persistente y secuencias de empleados](../../technical/softwareclock-employee-mapping.md); luego consultar marcas por documento guardado, sin redescubrimiento mensual. La decisión posterior de CU2 fija el workshift estructurado en KUME como origen de la propuesta inicial editable. El horario confirmado es independiente.
