# 001 — Implementación y evidencia

Estado: documentación preparada para revisión; no acredita integración o despliegue.

## Entrega

README enlaza la spec y docs/devops/operacion-oracle.md registra el flujo manual, estado/salud,
lock compartido, revalidación previa a activar, permisos existentes, fallos sin
fallback, retirada posterior de BACKEND_REVISION y reversión al workflow anterior.
Se satisfacen DOC01–DOC05 sin cambiar contrato, backend, VM ni variables GitHub.

Se sigue la rama y PR solicitados expresamente en esta sesión, por encima de la
convención habitual de docs directo a main. Cuatro commits: spec funcional,
spec técnica, plan e implementación. El frontend tiene el PR propietario de código.

## Verificación

- Seis pruebas operativas existentes aprobadas con fixtures ficticios.
- Enlaces relativos nuevos comprobados y contenido revisado contra la implementación
  frontend. Markdown de specs verificado con Prettier 3.9.10.
- No se modificaron scripts operativos. Su lint/formato se conserva y el CI del PR
  ejecuta sus controles existentes; no se afirma ejecución remota sin comprobarla.

Pendiente: integrar los PR y verificar una ejecución manual autorizada en Oracle.
Solo entonces retirar BACKEND_REVISION. Para volver al workflow anterior, revertir
el commit de implementación frontend y restaurar primero la variable con el SHA
instalado. No requiere migración ni cambio de VM.
