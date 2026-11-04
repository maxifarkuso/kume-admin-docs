# 001 — Obtención automática de la revisión backend

Estado: alcance solicitado por Maxi; implementación pendiente.
Fecha: 4 de noviembre de 2026.

## Objetivo

Actualizar la operación para que el workflow manual del frontend obtenga el SHA
del backend instalado por SSH, sin mantenimiento de BACKEND_REVISION.

La especificación funcional propietaria está en
[kume-admin-fe, 004](https://github.com/maxifarkuso/kume-admin-fe/blob/feat/automatic-backend-revision/docs/specs/004-backend-revision/spec.md).
Esta especificación cubre exclusivamente documentación operativa.

## Aceptación

- DOC01: explicar la consulta de estado y salud, la comprobación previa a activar,
  los fallos sin fallback y la coordinación mediante el lock existente.
- DOC02: detallar qué datos puede leer la consulta y los privilegios preexistentes,
  sin afirmar aislamiento de la cuenta ni proponer acceso a secretos.
- DOC03: indicar cuándo retirar BACKEND_REVISION y cómo volver al workflow anterior.
- DOC04: distinguir implementación, pruebas locales y verificación pendiente en VM.
- DOC05: rama desde main, PR compañero y cuatro hitos SDD separados, por instrucción
  explícita de esta sesión que prevalece sobre la convención de docs directo a main.

## Fuera de alcance

Modificar VM, permisos, variables GitHub, backend, autenticación o contrato HTTP;
desplegar o integrar PRs automáticamente.
