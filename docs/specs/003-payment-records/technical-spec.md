# Registro de pagos — especificación técnica

Fecha: 8 de noviembre de 2026. Estado: diseño e implementación local en curso; versionado, America/Montevideo y multipart aprobados expresamente por Maxi. Contrato local actualizado; sincronización inmutable pendiente.

## Fronteras y contrato

El [contrato canónico](../../../openapi.yaml) mantiene las operaciones de `expenses` y `categories`; la [API](../../technical/api-design.md) define filtros, errores, CSV y persistencia segura de archivos. La [especificación funcional](spec.md) define AC1–AC16. Los DTO se generan desde la revisión inmutable ya fijada en cada consumidor; antes de implementar se comparará con el contrato local. Las copias de referencia no se editan manualmente.

Backend: módulo `expenses` con dominio, aplicación/puertos, adaptadores Prisma y HTTP Fastify/TypeBox. `categories` es dueño del catálogo de rubros. Composición conecta colaboradores. Los handlers no acceden a Prisma; dominio y aplicación no importan frameworks, filesystem ni configuración. Frontend: feature `expenses`, API pública de `categories` para selección y composición desde app, sin ciclos. Se siguen las arquitecturas vigentes.

## Dinero y fechas

Decisión interna de implementación: representar importes como centésimos `bigint` en el núcleo, convertir desde/hacia texto decimal exacto en límites y persistir NUMERIC(12,2). No usar Number para sumar ni calcular totales. No serializar bigint directamente en JSON; devolver el texto canónico con dos decimales. Comprobar positivos, máximo contractual y rechazo de decimales extra.

Decisión temporal aprobada: reloj inyectado que resuelva la fecha civil de negocio en America/Montevideo, igual para fecha no futura y período inicial. Las fechas de pago se conservan como YYYY-MM-DD sin desplazamientos por UTC; los timestamps son instantes. Probar cambio de día y mes. Maxi aprobó esta zona horaria expresamente.

## Persistencia y atomicidad

Modelos `category`, `expense` y `receipt` con relaciones, tipos, checks e índices del [diseño de base](../../technical/backend/database-design.md). Migraciones aditivas revisables y carga inicial de rubros según alcance; sin seeds de arranque que sobrescriban ediciones, db push ni reset. No aplicar migraciones en producción ni dar por probada la persistencia a partir de unitarias.

Listar y totalizar con filtros idénticos y lectura consistente de items, conteos y suma. El total excluye anulados aunque el filtro los incluya. Orden canónico por fecha de pago y creación descendentes; identidad como desempate. El CSV usa el conjunto filtrado completo sin paginación, procesado sin cargar archivos binarios. Un rubro inactivo puede conservarse en un gasto existente; no puede asignarse como nuevo rubro. La validación de estado del rubro y escritura del gasto comparten transacción y coordinación con su desactivación.

## Comprobantes y compensación

Puerto de almacenamiento propiedad de aplicación: preparar archivo validado, confirmar clave opaca, abrir contenido autorizado y eliminar archivos no referenciados. Adaptador de disco con raíz configurada y persistente; el nombre original sirve solo para presentación. Nunca aceptar rutas proporcionadas por el cliente ni exponer storage_key en DTO públicos.

El backend actual no tiene parser multipart. Maxi aprobó incorporar el plugin oficial `@fastify/multipart`; se instaló y fijó 10.1.8, compatible con Fastify 5. No construir un parser multipart propio. Mantener límite JSON existente; aplicar límites específicos al upload sin ampliar globalmente el bodyLimit.

Procesar una única carga con límites de partes, campos y tamaño; rechazar campos/archivos inesperados, archivo vacío, exceso de tamaño o combinación extensión/MIME/firma inválida. La creación recibe `data` JSON y `receipt`, según OpenAPI. El reemplazo usa su operación independiente. Validar un máximo de 10.485.760 bytes mediante streaming limitado; no confiar en Content-Length. Preparar y validar antes de abrir transacción SQL.

Secuencia: temporal validado → archivo nuevo con clave opaca → transacción de gasto y metadatos → commit → limpieza del anterior. Si falla la base, compensar eliminando el nuevo. Si falla la limpieza, registrar un identificador técnico recuperable sin contenido privado; conservar referencias vigentes. El archivo anterior no se elimina antes del commit. No afirmar atomicidad distribuida entre base y disco.

Las descargas requieren sesión, resuelven la clave desde el gasto y devuelven tipo permitido y nombre seguro. Los gastos anulados permiten consulta y descarga, pero no edición ni reemplazo. Errores usan Problem Details según el contrato; no registrar archivos, contenido de formularios ni datos personales.

## Frontend

React Router para páginas y contexto de retorno; filtros y paginación en URL. TanStack Query con keys por filtros y página, sin reintento de mutaciones. Formularios React Hook Form/Zod para valores de edición y conversión explícita a DTO generado. Validar respuestas desconocidas con Zod, sin casts que sustituyan validación.

Crear y editar en páginas completas; comprobante obligatorio solo en creación. Reemplazo independiente con confirmación. Conservar borrador tras error y filtros al volver; no sustituir campos por un refresco de caché. Deshabilitar envíos pendientes sin prometer idempotencia ante respuesta perdida. Invalidar listado, total y detalle tras éxito.

El cliente compartido ya admite FormData sin imponer Content-Type; el navegador debe generar boundary. El transporte actual interpreta respuestas como JSON: para CSV y binarios se necesita una operación de descarga que reutilice manejo de errores y sesión. No duplicar autorización ni almacenar archivos/credenciales en localStorage. Abrir comprobantes mediante ruta autenticada en pestaña nueva, con enlace seguro.

CSV: formato, columnas y codificación canónicos. Revisar el tratamiento de texto que pueda interpretarse como fórmula en planillas; si requiere alterar el contenido exportado, proponer y aprobar la regla antes de cambiarla.

## Concurrencia aprobada

Gastos y rubros exponen versión inicial 1; PATCH exige la versión y al menos un campo editable. Acciones de estado exigen JSON con versión; reemplazo exige campo multipart `version` del gasto. Toda escritura aceptada incrementa atómicamente, incluso acciones de estado ya coincidente. La versión obsoleta devuelve 409 `VERSION_CONFLICT`, conserva borrador y exige recarga deliberada. No reintentar con versión nueva automáticamente.

La persistencia bloquea la fila de gasto y compara versión dentro de la misma transacción que cambia datos o referencia del archivo. Crear o cambiar de rubro bloquea y valida el rubro antes de escribir; desactivarlo utiliza el mismo bloqueo. Las operaciones del catálogo no adquieren bloqueos de gastos. Los archivos se preparan fuera de la transacción y se compensan al fallar. La comprobación real de carreras PostgreSQL sigue pendiente.

Los consumidores conservan su snapshot inmutable anterior y usan tipos/esquemas regenerados desde el contrato local aprobado durante esta implementación. Los chequeos de preview permiten indicar explícitamente ese archivo; no lo presentan como contenido del commit anterior. El chequeo ordinario debe seguir señalando la divergencia hasta autorizar el commit canónico y sincronizar las referencias. No publicar esta combinación como artefacto final.

## Verificación y entrega

Riesgo alto por dinero, archivos privados y persistencia. Unitarias de dominio/aplicación con reloj, IDs y puertos controlados; casos de fallos antes/después del commit y compensación. Frontend con React Testing Library para escenarios visibles, sin Playwright ni nueva suite de integración implícita. Pruebas unitarias no prueban SQL, filesystem real, proxy ni carreras PostgreSQL.

Ejecutar formato, lint/límites, typecheck, unitarias, contrato y build en ambos consumidores; validar Prisma y revisar migraciones. Registrar comandos y resultados, sin confundir compilación parcial con build de producción. Antes de datos reales siguen pendientes las verificaciones operativas del proyecto, respaldos y restauración consistente.

Entrega local revisable en ramas por feature; sin commit, push, merge, despliegue ni migraciones aplicadas por esta solicitud. Reversión conservadora: retirar pantallas/rutas y volver al artefacto anterior compatible; conservar datos y archivos, sin down destructivo.
