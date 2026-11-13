# Personal V1 — Evidencia de implementación

Fecha: 13 de noviembre de 2026. Estado: código publicado para revisión; no merge, despliegue ni migración aplicada.

## Etapas publicadas

| Etapa                   | Documentación (main) | Backend (feat/staff) | Frontend (feat/staff) |
| ----------------------- | -------------------- | -------------------- | --------------------- |
| Spec funcional          | a52d187              | 3a7cfc9              | fda498c               |
| Spec técnica y contrato | 05deb55              | a18e47a              | 9537d23               |
| Plan y tareas           | ca6503a              | 9ca51b6              | eac7800               |
| Implementación          | Este registro        | 97fe243              | e58e21d               |

[PR backend #8](https://github.com/maxifarkuso/kume-admin-be/pull/8) y [PR frontend #11](https://github.com/maxifarkuso/kume-admin-fe/pull/11), abiertos sin merge automático. Ambos consumidores fijan ca6503acea54d0c9d3e779d888ede6f3365f2ace y regeneran sus tipos; esta evidencia posterior no cambia el contrato.

## Resultado y validación local

P01–P08 implementados: fichas, búsqueda/estado, asignaciones actuales con ocupación exclusiva, bajas/reactivaciones y documentos privados. Versión común de ficha con comparación e incremento atómico, incluidas asignaciones y documentos; transferencia de responsable con ambas versiones. Bloqueos compartidos con catálogos y restricciones PostgreSQL preparadas en migración aditiva 202611130001_staff.

El frontend conserva contexto, borradores y archivo seleccionado, ofrece confirmaciones y recarga explícita, identifica ocupante y muestra inactivos de solo lectura. Se corrigió la pérdida de borradores al revalidar sesión: aplicación oculta/inerta durante la comprobación, sin conservar datos entre cuentas ni tras cierre o pérdida de sesión. Sigue el sistema visual aprobado, sin dependencias nuevas.

Backend: 88 pruebas en 15 archivos (67 previas), typecheck, lint/capas, format:check, build completo con Prisma nativo, contract:check y Prisma validate correctos. createApp compiló todas las rutas/esquemas sin conectar PostgreSQL. La comprobación de contrato cubre las 15 operaciones nuevas. Se conservan pruebas del adaptador de archivos extraído a infraestructura compartida.

Frontend: 64 pruebas en 14 archivos (48 previas), typecheck, lint/CSS/imports, format:check, build y contract:check correctos. Vite advierte chunk mayor a 500 kB. Una repetición concurrente del backend agotó el timeout de la prueba existente de scrypt; la suite completa volvió a pasar sin cambiar umbrales ni pruebas.

Revisión final frontend: selección de turno válido en destinos solo vespertinos, cancelación disponible ante errores de catálogo y errores documentales asociados al campo. Cubiertos por tres regresiones adicionales.

## Pendientes y límites

Las pruebas HTTP/repositorio y de React usan colaboradores controlados. No acreditan aplicación SQL, carreras PostgreSQL, integración completa entre módulos ejecutada contra base real, persistencia tras reinicio, proxy/HTTPS ni recuperación. Chromium headless con API local simulada no produjo DOM/captura antes del timeout; no se acredita revisión visual. No se instaló Playwright.

Migración preparada y revisable, sin ejecutar en Oracle ni en una base. Respaldo/restauración y demás condiciones del piloto conservan sus requisitos. Reversión mediante artefactos compatibles, conservando tablas/archivos y sin down destructivo. El paso 4 de pantallas no se da por cerrado por esta implementación.

## CI remoto comprobado

- Backend `97fe243cfa81927f69e3dc681409eb36564afafb`: [CI #47](https://github.com/maxifarkuso/kume-admin-be/actions/runs/43443686723) completada correctamente, incluidos checks de aplicación y entrega de imagen.
- Frontend `5d6aa2bef88e9d4fad660c45f746e85582d09db5`: [application checks #23](https://github.com/maxifarkuso/kume-admin-fe/actions/runs/43444591635) y [deployment checks #31](https://github.com/maxifarkuso/kume-admin-fe/actions/runs/43444591537) completados correctamente.

Resultados consultados en GitHub sobre las revisiones indicadas, sin merge de los PR ni despliegue. Los checks de entrega no equivalen a aplicar la migración de Personal ni a verificar sus flujos contra PostgreSQL real.
