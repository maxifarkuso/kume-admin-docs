---
name: kume-local
description: Preparar o retomar el servidor local de KUME, su automatización, migración desde Oracle y entrega de versiones desde GitHub; seguir etapas y evidencia del plan aprobado.
---

# KUME — Servidor local

Usar cuando Maxi pida preparar, implementar, ensayar o ejecutar el traslado completo
de KUME a la intranet, o retomar su plan y actualizaciones locales. No confundir
con migraciones de esquema de la utilidad kume-admin.

## Contexto

1. Leer [AGENTS.md](../../../AGENTS.md) y el
   [registro de decisiones](../../../docs/general/implementation-decisions.md).
2. Leer el [plan de servidor local](../../../docs/devops/plan-servidor-local.md),
   fuente propietaria de etapas, equipo de referencia, entrega GitHub y pendientes.
3. Leer [infraestructura y migración](../../../docs/devops/infraestructura-y-migracion.md),
   [stack](../../../docs/technical/stack-tecnologico.md) y
   [alcance](../../../docs/functional/alcance-prototipo.md).
4. Para inventario, distinguir evidencia histórica en
   [operación Oracle](../../../docs/devops/operacion-oracle.md) del estado actual.
   Revisar código/workflows reales de FE/BE antes de diseñar scripts o variables.
5. Si interviene la utilidad kume-admin, seguir su
   [skill](../kume-admin/SKILL.md) y las guías que esta exige. Para revisiones con
   Clock, revisar las dependencias citadas en el plan.

## Procedimiento

- Identificar etapa solicitada, último resultado comprobado y alcance autorizado
  en la sesión. La aprobación del plan no prueba instalación ni autoriza por sí
  sola ejecutar el corte, modificar Oracle o retirar infraestructura.
- Mantener acuerdos de equipo, Ubuntu CLI y UPS inicial omitida. No reabrirlos
  sin evidencia concreta de incompatibilidad o insuficiencia.
- Documentación: actualizar el plan y enlazar reglas existentes, sin duplicarlas.
  Implementación: trabajar sobre versiones explícitas y mecanismos reutilizables;
  separar preparación del host, respaldo, restauración y actualización.
- Preparar y verificar primero cambios revisables y ensayos autorizados. No pedir
  nuevamente una autorización ya otorgada; si falta para una acción real, presentar
  destino, etapa y efecto concretos después de completar preparación independiente.
- No inventar comandos, variables, hashes o rutas. Las opciones propuestas en el
  plan no son herramientas disponibles. No ejecutar descargas de ramas mutables
  sin revisión y verificación de integridad.
- En terminal guiada del usuario, un comando por vez y revisar su salida antes
  de avanzar. No solicitar secretos ni pegar archivos privados en chat.
- Restaurar en destino aislado; comprobar consistencia de base/archivos/cuentas.
  Las migraciones de esquema mantienen sus controles propios; no automatizarlas
  implícitamente al restaurar o iniciar servicios.
- No habilitar dos instalaciones con escrituras reales. Mantener origen y respaldo
  recuperables; si hubo escrituras locales, preservar esos cambios al volver atrás.
- No abrir acceso remoto, instalar runners ni conceder privilegios por inferencia.
  El mecanismo inicial propuesto descarga releases desde la intranet.

## Cierre

Registrar etapa, revisiones, verificaciones efectivamente realizadas, límites y
siguiente paso en el plan o memoria vinculada, sin datos privados. Diferenciar
documentado, implementado, instalado y verificado. No marcar migración completa
sin los criterios de aceptación de infraestructura y aceptación de Maxi.

Es una skill versionada de este repositorio. Puede invocarse como `kume-local` si
el cliente la descubre, o pidiendo leer este archivo; no instala un plugin global
ni agrega comandos al menú de kume-admin.
