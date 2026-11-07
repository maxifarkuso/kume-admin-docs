# Cursos y talleres — plan de implementación

Fecha: 7 de noviembre de 2026. Hitos revisables; estado y evidencia detallados en tasks.md.

| Orden | Hito                  | Entrega / condición de salida                                                                                                                            |
| ----- | --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1     | Especificación        | Alcance, criterios AC1–AC12, datos iniciales referenciados y exclusiones; preservar estado pendiente de diseño visual.                                   |
| 2     | Contrato y decisiones | Reconciliar OpenAPI, API, base y registro de decisión para versionado; verificar incompatibilidad y estrategia coordinada.                               |
| 3     | Persistencia y núcleo | Migraciones aditivas y carga inicial; dominio y casos de uso con unitarias; transacciones y restricciones revisadas.                                     |
| 4     | Adaptador HTTP        | Registrar doce operaciones protegidas; mapear resultados; verificar correspondencia con contrato canónico.                                               |
| 5     | Frontend              | DTO generados, listados/formularios, estado remoto, baja confirmada y conflicto sin perder borrador.                                                     |
| 6     | Verificación local    | Ejecutar controles de ambos repositorios, revisar diferencias y registrar fallas/bloqueos sin sustituirlas por supuestos.                                |
| 7     | Entrega y operación   | Con autorización de publicación: revisión canónica inmutable, commits por hito y PR enlazados. CI remoto, integración y despliegue permanecen separados. |

## Dependencias y límites

- binaries.prisma.sh debe estar permitido en la red del entorno para descargar las herramientas Prisma. No requiere el dominio ni acceso a la VM de Oracle.
- La base real de validación y el ensayo de carreras no se consideran existentes por disponer de migraciones.
- Las asignaciones todavía no están implementadas; su coordinación transaccional es requisito para la futura feature.
- La implementación de UI no marca terminado ni aprobado el paso 4 de diseño.
- No ejecutar cambios en producción, reset, commit ni push sin autorización expresa.
