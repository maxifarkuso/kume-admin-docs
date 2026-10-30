# KUME — Alcance del prototipo administrativo

**Fecha:** 29 de octubre de 2026  
**Estado:** alcance funcional, stack tecnológico y diseño técnico aprobados; pasos 1 a 3 completados; pendiente de diseño de pantallas e implementación.

Este documento permite retomar el proyecto en otra sesión con Maxi. Según confirmación del responsable del proyecto, los repositorios de frontend y backend están vacíos y no imponen limitaciones al stack aprobado. Todavía no se escribió código.

## 1. Objetivo

Centralizar los gastos ya pagados del centro educativo KUME para conocer cuánto se gastó por mes y rubro y consultar cada comprobante. Digitalizar también las fichas del personal, sus asignaciones a cursos y talleres y sus documentos.

Actualmente los comprobantes se comparten por WhatsApp, habitualmente con la información necesaria, pero no existe un registro consolidado.

## 2. Personas y responsabilidades

- **Usuaria inicial:** secretaria administrativa de KUME, sin conocimientos técnicos.
- **Desarrollo y mantenimiento:** Maxi, ingeniero en sistemas.
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

## 7. Ejecución local

- Aplicación local en una computadora, accesible desde el navegador.
- Sin despliegue en la nube.
- Sin usuario ni contraseña en el prototipo.
- Ejecución mediante **Docker Compose**.
- Primera instalación en **Windows**, con compatibilidad para **Linux**.
- Persistencia de datos y comprobantes al reiniciar o actualizar contenedores.
- Configuración sin depender de rutas específicas de Windows o Linux.

No se acordó acceso desde celulares u otras computadoras.

## 8. Copias de seguridad y restauración

Se deben implementar **scripts manuales de respaldo y restauración**, con instrucciones para Windows y Linux.

**Respaldo:**

- Generar un único archivo con la base de datos y todos los comprobantes.
- Incluir información sobre la versión del formato de respaldo.
- Permitir elegir dónde guardarlo.
- Informar claramente el resultado y los errores.

**Restauración:**

- Validar el respaldo.
- Pedir confirmación antes de reemplazar los datos actuales.
- Recuperar la base de datos y los comprobantes.
- Informar claramente el resultado y los errores.

No habrá copias automáticas ni se requiere una pantalla de restauración.

Antes de finalizar el prototipo se deberá **generar una copia y restaurarla en una instalación vacía**, verificando gastos, rubros, comprobantes, fichas de personal, cursos, talleres, asignaciones y documentos del personal.

## 9. Tecnología

El stack tecnológico está **aprobado** y se documenta en [Stack tecnológico](stack-tecnologico.md).

| Componente | Tecnología aprobada |
|---|---|
| Frontend | React + TypeScript + Vite |
| Backend | Node.js + TypeScript + Fastify |
| Base de datos | PostgreSQL |
| Acceso a datos y migraciones | Prisma |
| Archivos | Almacenamiento local persistente para comprobantes y documentos del personal |
| Ejecución | Docker Compose |

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
- Autenticación y múltiples usuarios.
- Despliegue en la nube.
- Copias de seguridad automáticas.

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
2. [x] **DONE — 30 de octubre de 2026:** Diseñar la base de datos, la API y el almacenamiento de comprobantes y documentos. Ver [diseño de base de datos](database-design.md), [diseño de API](api-design.md) y [contrato OpenAPI](openapi.yaml).
3. [x] **DONE — 30 de octubre de 2026:** Resolver detalles técnicos: validaciones, columnas del CSV, consulta de anulados, edición de gastos con rubros desactivados y reglas de fichas y asignaciones del personal. Decisiones registradas en el [diseño de base de datos](database-design.md), el [diseño de API](api-design.md) y el [contrato OpenAPI](openapi.yaml).
4. Diseñar las pantallas y convertir el alcance en tareas.
5. Implementar y verificar los flujos acordados.
6. Documentar instalación, uso, respaldo y restauración.

**Contexto adicional:** se mencionó el proyecto de ChatGPT “kume” y la conversación “Planilla de pagos por curso”, pero su contenido no se pudo consultar. Este documento se basa exclusivamente en las decisiones de esta sesión.
