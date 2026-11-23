# Maqueta de registro de horas

Fecha: 16 de noviembre de 2026. Estado: **interfaz y reglas funcionales aprobadas por Maxi** el 16/11/2026. Confirmación posterior a la entrega: «me gusta mucho la interfaz», con pedido de documentar para iniciar especificaciones y conexión con Clock. No cierra el paso 4.

## Ubicación

- Proyecto MagicPath: `473074895715196928`, Registro de horas · Docentes.
- Componente: `473074931341623296`, Detalle de maestra · Registro de horas.
- Nombre generado: `fiercely-stone-6964`.
- Revisión inicial compilada: `473074931341623297`. Revisión final compilada y comprobada: `473077607060094976`.

Se creó un proyecto independiente antes de descubrir el identificador del canvas histórico de KUME. Se conserva para evitar duplicar el prototipo; el proyecto histórico `467706881381666816` y sus bocetos no se modificaron. La composición utiliza el [sistema visual común](../../sistema-visual.md).

## Recorridos

- Registro de horas dentro de la ficha, filtro mensual y resumen de horas confirmadas, previstas y días por revisar.
- Tabla por día con dos bloques y cuatro posiciones de marcas; filtro Todos / Por revisar. Contenedor desplazable para consultar el mes completo.
- Revisar abre un panel modal lateral con horario previsto, marcas originales, asignación de marcas o ingreso manual, motivo opcional e historial.
- Guarda ajustes en memoria y recalcula los totales. Un tramo incompleto no se estima. Marcas adicionales se conservan y pueden señalarse como revisadas explícitamente.
- Panel de criterios con margen configurable, inicialmente 60 minutos.
- Actualizar es simulado; muestra última actualización y mensaje. El cabezal de revisión permite ver carga, vacío y error conservando datos.
- Salida con cambios solicita descartar o seguir editando. Validación de orden temporal y reutilización de una misma marca.

Escenarios ficticios: 3/11 falta entrada; 5/11 dos posibles entradas (08:00 y 08:02); 10/11 marca sin horario; 12/11 sin marcas; 16/11 en curso a las 10:30; futuros pendientes y fines de semana sin jornada prevista. El día de negocio ilustrado está fijado, no sigue el reloj real.

## Límites

No hay conexión real a Clock, autenticación KUME, persistencia al recargar ni escrituras al proveedor. Las marcas y asignaciones son ficticias. Cambiar de mes demuestra el filtro y las jornadas esperadas; los meses fuera de noviembre no tienen marcas de ejemplo. La consulta al abrir/cambiar mes está representada, no implementada contra un servicio.

La interpretación inicial de los ejemplos está predefinida. No es un motor general de emparejamiento ni resuelve cambios históricos de horarios, múltiples bloques arbitrarios o suplencias. El margen afecta la demostración de estados vencidos; el algoritmo general sigue pendiente. El rango 0–180 del editor es una restricción de demostración, no un acuerdo de producto. La confirmación de marcas excedentes ilustra una posible composición administrativa, no un contrato nuevo aprobado.

La navegación y las otras pestañas se muestran solo como contexto y están deshabilitadas en la maqueta. Los controles Revisión visual / Estado de prueba no pertenecen al producto. No hay conflicto de concurrencia implementado; su contrato deberá diseñarse antes de producción.

## Fuentes

Código: [composición](DetalleDeMaestraRegistroDeHoras.tsx), [revisión diaria](DayReview.tsx), [modelo de demostración](attendance.ts), [iconos](HoursIcon.tsx) y [estilos](RegistroDeHoras.css).

Capturas: [mes](mensual.png), [revisión de día](revision.png), [error de consulta](error.png) y [vista angosta](movil.png).

El código de referencia se conserva en esta carpeta, con módulos separados para datos/reglas de demostración, iconos, revisión de día y composición. No copiar directamente al frontend: adaptar a su arquitectura, componentes compartidos, formularios, TanStack Query, permisos y contratos canónicos.

- [Decisiones funcionales](../../../functional/registro-horas.md).
- [Hallazgos de API](../../../technical/softwareclock-api.md).

## Verificación

- Ambas revisiones compilaron en MagicPath; se inspeccionaron sus capturas remotas y las capturas locales de mes y revisión.
- TypeScript strict y noUncheckedIndexedAccess: sin errores, con herramientas aisladas bajo `work/`; no se agregaron dependencias al producto.
- Recorrido de Chromium local a 1440 px: 30 días de noviembre y 31 de diciembre, totales iniciales 56 h confirmadas / 160 h previstas / 4 días por revisar; tramos ambiguos excluidos. Completar la entrada del 3/11 aumenta el total a 60 h.
- Guardado con motivo vacío y autor/fecha en historial; conservación de originales; asignación de una entrada ambigua y revisión explícita del excedente.
- Validación de horas fuera de orden y reutilización de la misma marca; descarte de cambios; editor de margen; filtro de revisión y conservación de ajustes al cambiar de mes.
- Estados de carga, vacío y error de actualización conservando registros; botón de reintento simulado.
- Control mensual de 44 px; viewport 390 px sin desborde horizontal de la página (la tabla tiene su propio desplazamiento). Sin errores JavaScript de página en el recorrido.
- `git diff --check` y enlaces relativos de los documentos modificados verificados. OpenAPI no cambió; no se declararon contratos nuevos.

No es una auditoría completa de accesibilidad ni verificación del frontend/backend reales. No se probaron proveedor real desde el prototipo, persistencia, concurrencia, lector de pantalla, toda la matriz de navegadores ni recuperación de cambios al recargar. La aprobación visual de Maxi es una evidencia separada de estas verificaciones.

## Alcance de la aprobación y continuidad

Se conserva como referencia aprobada la revisión `473077607060094976` del componente `473074931341623296`, proyecto `473074895715196928`. No se modificó el canvas al registrar esta aprobación.

La aprobación comprende la composición mensual en la ficha, filtros, resumen, tabla por bloques, estados y panel de revisión con originales, ajuste manual, motivo opcional e historial. El mecanismo visual para revisar marcas excedentes queda como referencia para especificar el flujo, conservando todos los originales. No añade permisos para maestras ni escritura a Clock.

Quedan fuera de la UI de producto la barra Revisión visual, selector Estado de prueba, identidad/datos ficticios y avisos propios de la demostración. El reloj fijo, datos preasignados, almacenamiento en memoria, rango 0–180 y navegación deshabilitada son límites de la maqueta. No deben copiarse como reglas o arquitectura.

Continuar con la [preparación de especificaciones y conexión](../../../technical/registro-horas-preparacion.md), sin repetir las decisiones ya aprobadas.

## Evolución tras discovery del 23/11/2026

La [iniciativa 010](../../../specs/010-time-records/spec.md) consolida Q1–Q31 cerrados. Al implementar, adaptar la maqueta para horario propio editable con herencia inicial única, originales inmutables (sin sustitución manual de marcas reales), presentación/cálculo por minutos sin segundos, saldos informativos y excepciones/egreso. Los segundos visibles en las capturas o la lógica predefinida anterior describen la demostración histórica, no prevalecen sobre las reglas posteriores. No se creó una revisión nueva de MagicPath por esta documentación.
