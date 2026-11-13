# Personal — Especificación funcional

Fecha: 13 de noviembre de 2026. Estado: desarrollo autorizado por Maxi; no acredita implementación ni despliegue.

## Objetivo y alcance

Completar el último módulo funcional de V1: fichas de personal, asignaciones actuales a cursos/talleres y documentos privados. Uso inicial individual; se conserva concurrencia optimista para crecimiento. Las fichas no son cuentas de acceso. Maxi y Vicky mantienen iguales permisos.

## Criterios de aceptación

- P01: crear ficha activa con nombre, apellido, cédula uruguaya válida y única, teléfono y un rol (maestra, auxiliar o tallerista). Nacimiento, email, domicilio e ingreso opcionales. Buscar por nombre, apellido o cédula normalizada; activos por defecto, paginación y orden por apellido/nombre.
- P02: consultar/editar datos. Validar nacimiento anterior al día actual, ingreso no futuro, egreso no futuro ni anterior al ingreso. Fechas civiles en America/Montevideo. Rol informativo, sin restricciones sobre destinos.
- P03: asignar varias combinaciones curso/taller y turno. Solo persona y destino activos, turno ofrecido y un responsable por destino/turno. Taller cubre todos sus días. Cambiar/retirar sin historial. Conflicto identifica al ocupante y ofrece su ficha sin reemplazo automático.
- P04: inactivar con fecha de egreso y confirmación de las asignaciones concretas que se retiran. Conservar ficha/documentos. Ficha inactiva de solo lectura salvo reactivación; reactivar limpia egreso, sin recuperar asignaciones.
- P05: subir un archivo por vez con nombre libre, PDF/JPG/PNG de 1 a 10.485.760 bytes. Validar extensión, MIME y firma real. Consultar, abrir y descargar con sesión; eliminar con confirmación. Varias cargas por ficha; sin renombrado, reemplazo, tipos fijos, vencimientos ni alertas.
- P06: `version` común de ficha/datos/estado/asignaciones/documentos, inicialmente 1. Toda escritura aceptada sobre una ficha existente compara e incrementa su versión una vez. Versión obsoleta: 409 VERSION_CONFLICT, sin efectos parciales. Conservar borrador/archivo seleccionado; recarga explícita, sin reintento automático. Una nueva asignación invalida una confirmación de baja abierta previamente.
- P07: conservar contexto de búsqueda/página al navegar. Crear abre Datos; editar vuelve a ficha. Pestañas Datos, Asignaciones y Documentos; Marcas de horas deshabilitada como Próximamente. Carga, vacío, errores, éxito cerrable y confirmaciones accesibles según sistema visual vigente.
- P08: desactivación de catálogo o retirada de turno ocupado permanece bloqueada; no pueden aparecer asignaciones inválidas por carreras con catálogos o bajas de personal.

## Exclusiones y entrega

Sin CLOCK, horas, sueldos, múltiples roles, historial, carga masiva ni nuevos permisos/dependencias de producción. No se despliega ni se ejecutan migraciones productivas por este pedido. Código mediante ramas y PR sin merge automático. Hitos separados: especificación funcional, técnica/contrato, plan y tareas, implementación con evidencia.
