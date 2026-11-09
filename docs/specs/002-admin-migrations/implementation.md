# Implementación y evidencia — 002

Fecha: 7 de noviembre de 2026. Estado: implementado y verificado localmente con
colaboradores controlados; pendiente de instalación y validación real en Oracle.
Sin commits, push, cambios de permisos externos ni despliegues. El checkout llegó
limpio en work, sin referencia main local; se comprobó su estado y se creó main en
la misma revisión, sin descartar ni mover cambios ajenos.

## Resultado

- Dispatcher Bash preserva consultas y añade grupo migraciones/ayuda al menú.
- CLI Python compone workflow, almacenamiento privado y adaptador de efectos;
  sin dependencias de producción nuevas. Instalación ampliada requiere el paquete
  completo, no solamente el archivo Bash histórico.
- Configuración explícita de destino, revisión/origen, SQL verificador inicial y
  final aprobados. Snapshot desde Git, checksum de migraciones, recursos y conexión
  filtrada, DNS, esquema public, identidad física y releases estables entre etapas.
- Contenedor limitado y local; npm con scripts deshabilitados y aprobación/rebuild
  limitado a dos paquetes. Prisma permanece en 6.19.0.
- Dump CUSTOM privado con índice y checksum, sin afirmar restauración; deploy y
  baseline excepcional separados con confirmación literal y revalidación.
- Journal atómico con intención previa, incertidumbre conservada y bloqueo de otras
  operaciones con SQL incierto. Inicialización interrumpida permite inspeccionar,
  verificar y registrar, sin repetir db execute. Retirada limitada a ID/label propio.
- Instrucciones, skill local, guías, índice y CI actualizados. No cambia API/OpenAPI,
  esquema de negocio ni reglas propietarias de los catálogos.

## Verificaciones locales

- 39 tests unittest, incluidos los nueve originales: correctos. Dobles de
  Docker/SQL/npm y filesystem temporal; fixture Git local para snapshot/checksum.
  Cubren cancelación/EOF, host/conexión erróneos, pending, recursos insuficientes,
  destino físico cambiado, respaldo corrupto/fallido, herramientas/npm previos y
  aprobación restringida, migración fallida, historia divergente, inicialización,
  interrupciones, locks no bloqueantes y retirada ajena rechazada.
- bash -n, ShellCheck 0.10.0 y shfmt 3.12.0: correctos. Binarios de verificación
  descargados en work fuera del producto, con los SHA-256 fijados en CI comprobados.
- Compilación sintáctica Python, Ruff 0.14.4 lint y formato: correctos; herramienta
  solo de verificación local en work, sin dependencia nueva en producción.
- Ambas ayudas, git diff --check, enlaces relativos y bloques Markdown de los
  documentos tocados: correctos. No cambia OpenAPI; no corresponde regeneración.
- Revisión manual del diff y mapa por responsabilidad: oracle-admin.sh despacha;
  cli.py compone; workflow.py decide etapas; runtime.py concentra efectos externos;
  storage.py persiste evidencias/locks; tests/ usa colaboradores controlados.
  No hay .clean ni capas declaradas; revisión manual de imports y límites, sin
  atribuir ejecución a scripts de análisis de la skill cloud no materializados.

## Riesgo y pendientes

Riesgo alto por habilitar escrituras y coordinar concurrencia. Estas pruebas no
acreditan SQL PostgreSQL real, recuperación, restauración, OOM, permisos Docker,
concurrencia de pipelines ni compatibilidad efectiva de todas las imágenes/npm.
No se instaló Node/npm/Prisma ni se creó un contenedor de producto en este host.

Antes de uso real: revisar SHA y todos los checksums de la distribución completa,
preparar los verificadores específicos del SQL del proyecto, confirmar acceso y
privilegios existentes, verificar que los workflows instalados cooperen con el lock
y suspender externamente los restantes. Probar en PostgreSQL aislado con datos
ficticios y luego obtener autorización explícita para destino y ventana de Oracle.
No modificar privilegios para hacer pasar una comprobación.

Rollback de herramienta: recuperar la distribución anterior conservada, con sus
huellas originales. No elimina los nuevos journals ni revierte SQL; cualquier
recuperación de datos exige inspección, decisión y restauración/corrección autorizadas
por separado. No hay down migration, reset, restauración ni despliegue implícitos.

Runbook propietario: [migraciones-admin.md](../../devops/migraciones-admin.md).

## Publicación — 8 de noviembre de 2026

Maxi autorizó subir los cambios. Implementación publicada en main de docs, commit
`3c262bd2a92702228515d6ef7596d136e5df29a1`, después de incorporar los avances remotos sin descartarlos.
39 pruebas locales correctas nuevamente. Se agregó el
[paso a paso de gastos](../../devops/migraciones-payment-records.md), fijado al SQL
del backend feat/payment-records; no se ejecutó SQL en Oracle.

## Corrección del sondeo de npm — 8 de noviembre de 2026

En la preparación guiada en Oracle, npm install devolvió 0 y npm --help devolvió 1
con ayuda reconocible y approve-scripts anunciado. La primera implementación trató
esa ayuda como error y dejó preparar=failed, código 1. El contenedor temporal quedó
activo; no se ejecutó SQL de migración. La consulta manual Prisma --version mostró
6.19.0 y motores disponibles; no se cambió por eso el resultado fallido del journal.

Se reprodujo el fallo localmente antes del cambio. Ahora solo el sondeo de ayuda
acepta 0/1, condicionado a contenido reconocido; las operaciones de instalación,
aprobación y reconstrucción conservan su tratamiento de errores. Se rechaza ayuda
inválida sin exponer su contenido. Suite completa: 42 pruebas correctas, Ruff lint/
formato y diff --check correctos. La recuperación operativa requiere retirar el
contenedor propio, actualizar y comenzar una nueva preparación, sin forzar etapas.
Validación de esa corrección en Oracle y aplicación de SQL siguen pendientes.
