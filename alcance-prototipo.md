# KUME — Alcance del prototipo administrativo

**Fecha:** 29 de octubre de 2026  
**Estado:** alcance funcional acordado; pendiente de diseño técnico e implementación.

Este documento permite retomar el proyecto en otra sesión con Maxi. Hasta ahora no se revisaron los repositorios de frontend y backend ni se escribió código.

## 1. Objetivo

Centralizar los gastos ya pagados del centro educativo KUME para conocer cuánto se gastó por mes y rubro y consultar cada comprobante.

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

Antes de finalizar el prototipo se deberá **generar una copia y restaurarla en una instalación vacía**, verificando gastos, rubros y comprobantes.

## 9. Tecnología

**Decisiones confirmadas:**

| Componente | Tecnología |
|---|---|
| Frontend | React y TypeScript |
| Backend | TypeScript |
| Base de datos | PostgreSQL |
| Ejecución | Docker Compose |

**Recomendaciones pendientes de validar con Maxi:**

- Vite para el frontend.
- Node.js con Fastify para el backend.
- Prisma para acceso a datos y migraciones.
- Almacenamiento local persistente para comprobantes.

Next.js se mencionó como alternativa, pero **no fue seleccionado**.

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

## 11. Personal y CLOCK — TBD

Este módulo queda postergado. La idea original incluía:

- Ficha del personal con datos básicos.
- Rol de maestra, auxiliar o tallerista y curso a cargo.
- Documentos y formularios, por ejemplo manipulación de alimentos.
- Registro de marcas y eventual integración con CLOCK.

Todavía no se conoce cómo integrar CLOCK. **No forma parte del prototipo de gastos.**

## 12. Próximos pasos con Maxi

1. Revisar ambos repositorios de código y confirmar las herramientas complementarias.
2. Diseñar la base de datos, la API y el almacenamiento de comprobantes.
3. Resolver detalles técnicos: validaciones, columnas del CSV, consulta de anulados y edición de gastos con rubros desactivados.
4. Diseñar las pantallas y convertir el alcance en tareas.
5. Implementar y verificar los flujos acordados.
6. Documentar instalación, uso, respaldo y restauración.

**Contexto adicional:** se mencionó el proyecto de ChatGPT “kume” y la conversación “Planilla de pagos por curso”, pero su contenido no se pudo consultar. Este documento se basa exclusivamente en las decisiones de esta sesión.
