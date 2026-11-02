# KUME — Alcance del prototipo administrativo

**Fecha:** 29 de octubre de 2026
**Actualización:** 2 de noviembre de 2026 — autenticación simplificada confirmada con GrillMe y restitución de tareas finalizadas.
**Estado:** alcance y stack actualizados y confirmados; diseño funcional de base y API conservado; diseño técnico y contrato de autenticación completos; implementación de seguridad y operación pendientes; diseño de pantallas en curso (paso 4); implementación de KUME pendiente; infraestructura básica cloud probada.

Este documento permite retomar el proyecto en otra sesión con Maxi. Según confirmación del responsable del proyecto, los repositorios de frontend y backend están vacíos y no imponen limitaciones al stack aprobado. Todavía no se implementó KUME. Se ejecutó una API temporal de prueba en Oracle para verificar Fastify, PostgreSQL y persistencia; no es código del producto.

## 1. Objetivo

Centralizar los gastos ya pagados del centro educativo KUME para conocer cuánto se gastó por mes y rubro y consultar cada comprobante. Digitalizar también las fichas del personal, sus asignaciones a cursos y talleres y sus documentos.

Actualmente los comprobantes se comparten por WhatsApp, habitualmente con la información necesaria, pero no existe un registro consolidado.

## 2. Personas y responsabilidades

- **Usuaria inicial:** secretaria administrativa de KUME, sin conocimientos técnicos.
- **Desarrollo y mantenimiento:** Maxi, ingeniero en sistemas.
- **Acceso:** Vicky (secretaria) y Maxi (técnico), con cuentas individuales y los mismos permisos de acceso completo a los datos del prototipo.
- **Administración técnica:** Maxi administra cuentas, atiende alertas y ejecuta restauraciones. Infraestructura y respaldos bajo control de KUME, con recuperación accesible a la institución.
- **Fecha de entrega:** sin fecha comprometida.

## 3. Registro de gastos

Se podrán **crear, consultar, editar y anular** gastos ya pagados.

| Campo | Definición |
|---|---|
| Fecha de pago | Determina el mes del gasto |
| Importe | Pesos uruguayos —UYU— con dos decimales |
| Destinatario o proveedor | Texto libre |
| Concepto | Descripción de qué se pagó |
| Rubro | Selección de un rubro administrable |
| Comprobante | Un único archivo obligatorio |

**Reglas acordadas:**

- Una compra de octubre pagada en noviembre se contabiliza en noviembre.
- Se admiten comprobantes **PDF, JPG y PNG, de hasta 10 MB**.
- No se puede guardar un gasto sin comprobante.
- El comprobante puede reemplazarse al editar.
- No se requiere adjuntar una factura adicional.
- La eliminación se realiza mediante un **flag de anulación**.
- Los gastos anulados se conservan para consulta y no suman en los totales.

## 4. Administración de rubros

CRUD sencillo para crear, consultar, modificar y dar de baja rubros.

Rubros iniciales:

- Mantenimiento.
- Materiales.
- Servicios.

Los rubros con gastos asociados se **desactivan mediante un flag**, conservando sus asociaciones históricas. No deberán ofrecerse para nuevos gastos.

El tratamiento de rubros nunca utilizados puede resolverse durante el diseño técnico.

## 5. Consulta y exportación

La pantalla de gastos tendrá:

- Mes actual seleccionado por defecto.
- Listado de gastos.
- Total del período, excluyendo anulados.
- Filtros por fechas de pago y rubro.
- Acceso al comprobante de cada gasto.
- Posibilidad de consultar gastos anulados.
- Exportación del listado filtrado a **CSV**.

No se necesita exportación con formato de Excel.

## 6. Inicio de uso

Se comenzarán a registrar gastos cuando el sistema esté disponible.

La carga histórica desde marzo queda fuera del prototipo. La **importación por lote** queda para una versión posterior.

## 7. Ejecución cloud y alternativa local

### Modalidad inicial: Oracle Cloud Always Free

- Backend alojado en una máquina virtual de Oracle Cloud Infrastructure elegible para Always Free, con Linux soportado y Docker Compose.
- Una sola VM inicialmente, con API Fastify y PostgreSQL en contenedores separados y volúmenes persistentes para base de datos y archivos. PostgreSQL no se expone a internet.
- Frontend React + TypeScript + Vite compilado y servido por el proxy de la VM Oracle, bajo el mismo origen HTTPS que la API (`/api/v1`). Decisión confirmada el 2 de noviembre; sustituye la alternativa Cloudflare Pages. Sin servicios locales para el uso diario.
- Acceso desde distintas computadoras mediante navegador. Prioridad de escritorio; el uso completo desde celulares queda fuera del MVP.
- Piloto con datos reales y demo separada con datos y archivos ficticios y cuenta propia.
- Dos usuarios, Maxi y Vicky, con contraseñas individuales almacenadas como hash en un archivo de secrets del servidor, sin tabla de usuarios. Mismos permisos, cierre manual y vencimiento tras 8 horas de inactividad. Cambios de contraseña manuales a cargo de Maxi; sin recuperación por correo, registro público ni pantalla de administración de usuarios. Limitar intentos por cuenta y por IP mediante pausas temporales. Proteger pantallas, operaciones y archivos mediante una sesión válida. Ver [autenticación y tareas adicionales](autenticacion-prototipo.md).
- Ambos pueden consultar y modificar los datos del sistema; administración de cuentas y restauraciones a cargo de Maxi.
- Archivos privados y descargas autorizadas. Credenciales administrativas fuera del navegador y del repositorio.
- Persistencia al reiniciar y actualizar contenedores. Configuración portable, sin rutas absolutas dependientes de Windows o Linux.
- HTTPS y autenticación deben estar verificados antes de habilitar datos reales.

### Costo y disponibilidad

El objetivo es mantener el costo total en **USD 0**, incluyendo piloto, demo y respaldos. No hay presupuesto pago preaprobado ni contrataciones automáticas. Distinguir Always Free de los créditos promocionales de tiempo limitado.

No se realizará un cálculo de consumo anual para el MVP. Sí se verificarán cuotas, espacio y condiciones necesarias para desplegar y respaldar, y se observarán los límites disponibles antes de comprometer el uso. No se eliminarán datos automáticamente para liberar capacidad.

Se aceptan pausas o demoras de servicios gratuitos durante demo y piloto, con mensajes claros de indisponibilidad. Oracle puede recuperar instancias consideradas inactivas y la modalidad gratuita no garantiza disponibilidad mediante SLA. Revisar continuidad antes de depender diariamente del sistema.

### Alternativa futura: migración completa a intranet

Si los límites o las condiciones gratuitas comprometen el uso, se evaluará migrar a un equipo del instituto. Se conservarán Node.js, Fastify, Prisma, PostgreSQL y Docker Compose; Oracle se usa como infraestructura, sin reemplazar la API por servicios propietarios. Supabase no forma parte de la arquitectura elegida.

La migración deberá trasladar base de datos, archivos, cuentas y configuración, y servir el frontend desde la red local. El funcionamiento diario no dependerá de servicios cloud. Los cambios de contraseña se realizan manualmente en secrets, sin servicio de correo. Los respaldos externos pueden requerir internet; sus dependencias y alternativas deberán documentarse.

El acceso inicial será solo desde la intranet, sin acceso remoto. El equipo deberá permanecer encendido durante el uso; equipo, sistema operativo soportado y mantenimiento se resolverán antes del traslado. Windows o Linux son alternativas a verificar, no instalaciones locales ya probadas.

El MVP documentará dependencias y exportación y verificará portabilidad de datos y archivos. El despliegue local completo se implementará cuando se decida migrar. Se requerirá ensayo, respaldo consistente, ventana sin escrituras, validación del destino y posibilidad de volver atrás sin perder cambios; no habrá dos instalaciones aceptando escrituras en paralelo. La migración no se considera ejecutada por contar con Docker Compose.

Ver [infraestructura cloud y migración local](infraestructura-y-migracion.md).

## 8. Copias de seguridad y restauración

Se deben implementar respaldos automáticos diarios y herramientas de restauración documentadas. La automatización y el destino deben verificarse dentro del objetivo de costo cero.

**Respaldo:**

- Incluir PostgreSQL, comprobantes, documentos del personal y configuración necesaria para recuperar el sistema y sus cuentas.
- Generar una unidad lógica de recuperación versionada, cifrada y verificable, con consistencia entre base y archivos. Un dump de PostgreSQL no incluye el volumen documental.
- Guardar las copias fuera de la VM y de Oracle, en almacenamiento institucional bajo control de KUME; Google Drive es el candidato conversado, pendiente de configuración y verificación.
- Conservar 30 días y custodiar las claves de descifrado de forma recuperable y separada de las copias.
- Objetivo de pérdida tolerable de hasta 24 horas, condicionado a copias exitosas y atención de fallas.
- Alertar a Maxi si falla una copia e informar resultado y errores. No considerar configuradas las alertas sin comprobar su entrega.
- Mantener una ejecución manual documentada para respaldo previo a mantenimiento o migración.

**Restauración:**

- Validar formato, versión e integridad del respaldo.
- Pedir confirmación antes de reemplazar datos existentes.
- Recuperar base, archivos y acceso de cuentas; informar resultado y errores.
- No se requiere pantalla de restauración; tarea administrativa a cargo de Maxi.

Antes del uso real se deberá **generar una copia y restaurarla en un entorno vacío**, verificando gastos, rubros, comprobantes, fichas de personal, cursos, talleres, asignaciones, documentos y acceso autorizado. Repetir una prueba de restauración trimestralmente.

La disponibilidad de espacio para retener 30 días, el mecanismo de automatización, las claves y el destino externo siguen pendientes de validación. El respaldo debe seguir siendo aplicable tras migrar a intranet.

## 9. Tecnología

El stack tecnológico está **aprobado** y se documenta en [Stack tecnológico](stack-tecnologico.md).

| Componente | Tecnología aprobada |
|---|---|
| Frontend | React + TypeScript + Vite |
| Backend | Node.js + TypeScript + Fastify |
| Base de datos | PostgreSQL |
| Acceso a datos y migraciones | Prisma |
| Archivos | Volumen persistente del servidor, con acceso mediante la API |
| Ejecución | Docker Compose, inicialmente en Oracle Cloud Always Free |
| Alternativa de despliegue | Equipo local del instituto, con migración completa a intranet |

**Repositorios:**

- Frontend: https://github.com/maxifarkuso/kume-admin-fe
- Backend: https://github.com/maxifarkuso/kume-admin-be
- Documentación: https://github.com/maxifarkuso/kume-admin-docs

## 10. Fuera de esta versión

- Cobranzas a familias y cuotas de cursos.
- Sueldos.
- Cuentas pendientes, vencimientos y pagos parciales por completar.
- Monedas distintas de UYU y conversiones.
- Carga histórica e importación por lote.
- Catálogo administrable de proveedores.
- Exportación con formato de Excel.
- Registro público, recuperación de contraseña por correo, pantalla de administración de usuarios y permisos diferenciados.
- Uso completo desde celulares.
- Ejecución de la migración completa a intranet dentro del MVP inicial; se documenta su preparación.
- Acceso remoto a la intranet.

## 11. Registro de personal

### Objetivo

Digitalizar la información del personal, hoy conservada en documentos físicos, centralizando datos personales, rol, asignaciones y archivos en una ficha.

### Ficha y datos personales

Se podrán registrar, consultar y editar fichas de personal.

| Campo | Regla |
|---|---|
| Nombre | Obligatorio |
| Apellido | Obligatorio |
| Cédula | Obligatoria y única |
| Teléfono | Obligatorio |
| Fecha de nacimiento | Opcional |
| Correo electrónico | Opcional |
| Domicilio | Opcional |
| Fecha de ingreso | Opcional |
| Rol | Un único rol: maestra, auxiliar o tallerista |
| Estado | Activo o inactivo |
| Fecha de egreso | Obligatoria al marcar a la persona como inactiva |

La baja será lógica: se conserva la ficha y sus documentos. Al inactivar a una persona se liberan sus asignaciones actuales para permitir asignar a otra.

### Listado y búsqueda

- Búsqueda por nombre, apellido o cédula.
- Personal activo visible por defecto y posibilidad de consultar personal inactivo.
- No se requieren otros filtros de búsqueda en esta versión.

### Asignaciones

- Una persona puede registrarse sin asignaciones y recibirlas más adelante.
- Puede tener varias asignaciones a cursos o talleres.
- Cada combinación de curso o taller y turno admite una sola persona activa a cargo.
- Se mantiene únicamente la asignación actual, sin historial de responsables.
- Se puede retirar o cambiar una asignación.

### Cursos

Catálogo administrable con esta carga inicial:

| Curso | Nivel | Nombre interno | Días | Turnos |
|---|---|---|---|---|
| Maternal | 0 | — | Lunes a viernes | Matutino y vespertino |
| Nivel 1 | 1 | Kiru | Lunes a viernes | Matutino y vespertino |
| Nivel 2 | 2 | Cururu | Lunes a viernes | Matutino y vespertino |
| Nivel 3 | 3 | Capibara | Lunes a viernes | Matutino y vespertino |
| Nivel 4 | 4 | Ñurumi | Lunes a viernes | Matutino y vespertino |
| Nivel 5 | 5 | Mamboreta | Lunes a viernes | Matutino y vespertino |
| Escolares | Escolares | Pangui | Lunes a viernes | Matutino y vespertino |

Turnos de referencia:

- **Matutino:** de 8:00 a 12:00.
- **Vespertino:** de 13:00 a 17:00.

Cada asignación selecciona curso y turno.

### Talleres

Catálogo administrable con esta carga inicial:

| Taller | Días iniciales | Turnos |
|---|---|---|
| Música | Lunes | Matutino y vespertino |
| Arte | Martes | Matutino y vespertino |
| Gimnasia | Miércoles | Matutino y vespertino |

- Cada taller puede tener varios días de la semana, modificables desde su administración.
- Para simplificar el prototipo, solo se registran días y turno; no se modela el horario exacto de cada taller.
- La persona asignada cubre todos los días configurados para el taller en el turno seleccionado; no elige un subconjunto de días.

### Baja de cursos y talleres

- Se desactivan mediante un flag, sin borrado físico.
- **No se permite desactivar un curso o taller mientras tenga una persona a cargo en cualquiera de sus turnos.**
- Primero deberán retirarse o cambiarse las asignaciones.
- Los cursos y talleres inactivos no estarán disponibles para nuevas asignaciones.

### Documentos del personal

Cada ficha tendrá una pestaña de documentos:

- Varios archivos por persona.
- Cada archivo tendrá un nombre asignado libremente.
- Formatos admitidos: **PDF, JPG y PNG**, hasta **10 MB por archivo**.
- Posibilidad de subir, consultar y descargar archivos.
- Sin catálogo fijo de tipos de documento.
- Sin fechas de vencimiento, alertas ni control de documentación faltante.

Los respaldos y la restauración deberán incluir estos documentos, además de los comprobantes de gastos y todos los datos del sistema.

### Fuera del alcance de personal

- Registro de marcas e integración con CLOCK.
- Horarios exactos de talleres.
- Historial de asignaciones.
- Múltiples roles por persona.
- Vencimientos y alertas de documentos.

CLOCK continúa pendiente para una versión futura; todavía no se conoce su mecanismo de integración.

## 12. Próximos pasos con Maxi

1. [x] **DONE — 29 de octubre de 2026:** Revisar ambos repositorios de código y confirmar las herramientas complementarias. El responsable confirmó que ambos repositorios están vacíos, sin limitaciones previas, y aprobó el [stack tecnológico](stack-tecnologico.md).
2. [x] **DONE — 30 de octubre de 2026:** Diseñar la base de datos, la API y el almacenamiento de comprobantes y documentos. Completado funcional conservado; autenticación y operación se siguen como tareas adicionales independientes. Ver [diseño de base de datos](database-design.md), [diseño de API](api-design.md) y [contrato OpenAPI](openapi.yaml).
3. [x] **DONE — 30 de octubre de 2026:** Resolver detalles técnicos: validaciones, columnas del CSV, consulta de anulados, edición de gastos con rubros desactivados y reglas de fichas y asignaciones del personal. Las ampliaciones cloud no reabren estas decisiones. Decisiones registradas en el [diseño de base de datos](database-design.md), el [diseño de API](api-design.md) y el [contrato OpenAPI](openapi.yaml).
4. [ ] **EN CURSO — 1 de noviembre de 2026:** Diseñar las pantallas y convertir el alcance en tareas. Navegación y bocetos estáticos de gastos y personal aprobados. Pendientes: catálogos, login, intentos limitados, cierre y expiración de sesión, identificación de demo, indisponibilidad cloud, prototipo interactivo, documentación final y backlog. Sesión pausada hasta disponer de créditos de MagicPath; continuación prevista para el 2 de noviembre. Retomar desde la [memoria para el diseño de pantallas](continuacion-diseno-pantallas.md). No marcar como completado sin confirmación expresa de Maxi.
5. Implementar y verificar los flujos acordados.
6. Documentar despliegue cloud en Oracle, uso, cuentas, respaldo/restauración y preparación de migración a intranet; comprobar recuperación y carga representativa antes del piloto.

**Tareas adicionales — 2 de noviembre de 2026:** el alcance, diseño técnico y contrato de autenticación están completos; quedan pantallas, implementación, despliegue y verificación. El detalle y los criterios para cerrar las tareas están en [autenticación del prototipo](autenticacion-prototipo.md). Concurrencia, respaldos diarios, HTTPS y preparación de migración continúan pendientes según [infraestructura](infraestructura-y-migracion.md), sin reabrir los pasos 2 y 3. El paso 4 conserva su estado en curso.

**Contexto adicional:** se mencionó el proyecto de ChatGPT “kume” y la conversación “Planilla de pagos por curso”, pero su contenido no se pudo consultar. Este documento se basa exclusivamente en las decisiones de esta sesión.

## 13. Registro del cambio de ejecución — 1 de noviembre de 2026

Maxi confirmó revisar los requisitos con GrillMe y luego conservar la API Node.js/Fastify, Prisma y PostgreSQL. Se eligió Oracle como infraestructura cloud y se probó una VM con Docker Compose, Fastify y consulta SQL real; la persistencia de PostgreSQL sobrevivió a recrear su contenedor. Las funciones de gastos, personal, catálogos y CSV no cambian por esta decisión. Autenticación, HTTPS, archivos del producto, respaldos, carga real y migración local aún no están implementados ni verificados. El paso 4 sigue en curso y no se marca completo.
