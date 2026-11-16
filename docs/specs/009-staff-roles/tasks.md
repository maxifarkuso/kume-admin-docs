# Tareas y evidencia

- [x] Solicitud y diseño preparados.
- [x] Implementación en branch `fix/staff-roles`.
- [x] Verificación local.
- [ ] Integración y despliegue (fuera de esta tarea).

## Verificación — 16 de noviembre de 2026

- fe: 65 pruebas aprobadas; typecheck, lint, contract:check, build y format:check aprobados.
- be: 93 pruebas aprobadas; typecheck, lint, contract:check, build y format:check aprobados.

Riesgo: medio en cambios de contrato/persistencia; bajo en estilos. Pruebas unitarias y controles estáticos locales; sin pruebas integradas en navegador ni PostgreSQL real. Migraciones preparadas sin aplicar. Branches independientes desde main; al integrar varios cambios, reconciliar OpenAPI y regenerar snapshots desde la revisión documental conjunta. Sin push, PR remoto, merge ni despliegue.
