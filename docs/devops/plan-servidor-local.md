# KUME — Plan de servidor local

Fecha: 16 de noviembre de 2026 (America/Montevideo).
Estado: **camino de preparación acordado con Maxi; implementación y ejecución pendientes**.
No acredita compra del equipo, instalación de Ubuntu, scripts disponibles, workflows
adaptados ni migración realizada. La solicitud actual autoriza documentar el plan
y crear su skill interna, no operar Oracle ni el equipo futuro.

## Objetivo y decisiones de esta sesión

Preparar un camino repetible para trasladar KUME desde Oracle a un equipo del
instituto, ensayarlo y habilitarlo únicamente después de verificar recuperación
y funcionamiento en la intranet. Conservar el stack aprobado y evitar dos
instalaciones aceptando escrituras reales simultáneamente.

| Tema | Acuerdo o referencia |
| --- | --- |
| Uso previsto | Hasta cinco personas, con actividad baja; no es una medición de concurrencia. Las cuentas actuales siguen siendo las del diseño de autenticación. |
| Equipo de referencia | Lenovo ThinkCentre Tiny M910q reacondicionado, Intel Core i5-6500T, 8 GB DDR4 y SSD de 256 GB. Compra no confirmada. |
| Dimensionamiento | Configuración considerada razonable para empezar con KUME dedicado; validar RAM, disco y rendimiento en el ensayo. No exigir ampliación inicial a 16 GB/512 GB sin evidencia. |
| Sistema | Ubuntu Server 24.04 LTS, AMD64/x86_64, sin entorno gráfico; administración por terminal y SSH. Revisar ISO oficial y checksum al instalar. |
| Red | Ethernet; acceso inicial solo desde intranet, nombre interno y HTTPS. Sin apertura de acceso remoto por esta decisión. |
| UPS | Maxi decide omitirla inicialmente. Un corte interrumpe el servicio; comprobar recuperación posterior y mantener respaldos externos. |
| Implementación | Primero preparación y copia de ensayo; después corte definitivo coordinado. Automatización por etapas, con verificaciones. |
| Actualizaciones | Propuesta inicial aceptada como camino de trabajo: GitHub construye y el servidor descarga una versión explícita mediante un comando manual. Diseño exacto pendiente. |

Ficha comercial de referencia: [Lenovo 8 GB/256 GB en BuyTech](https://www.buytech.uy/catalogo/buytech/pcs/equipos-pc/recertificados/equipo-ultra-mini-pc-lenovo-tiny-m910q-intel-core-i5-6500t-31ghz-ram-8gb-ddr4-ssd-256gb-2x-dport-vga-w10-pro-ci5lenovom910qtinypz/).
Precios conversados orientativos: USD 183 por esa configuración, USD 415 por
16 GB/512 GB y USD 107 por un disco externo de 1 TB. No son cotizaciones ni
autorización de compra; revalidar precio, stock, garantía y estado del SSD.
El disco externo no se considera comprado ni destino de respaldo configurado.

La [guía de infraestructura](infraestructura-y-migracion.md) conserva las reglas
de seguridad, consistencia, corte y aceptación. Este documento es su plan de
ejecución futura; no reemplaza las guías de migraciones de esquema.

## Cómo retomar

Invocar la skill interna **kume-local** en este repositorio, por ejemplo:
«Usá kume-local para preparar el ensayo de migración a la Lenovo».
Si la herramienta no la descubre automáticamente, pedir que lea
`.agents/skills/kume-local/SKILL.md`. No es un comando de shell ni un plugin global.

Al retomar, identificar la etapa, revisar decisiones y evidencia existentes y
continuar desde el último resultado comprobado. No repetir preguntas resueltas
ni confundir una lista de tareas con una instalación terminada.

## Etapas y evidencia requerida

| Etapa | Trabajo | Evidencia para avanzar |
| --- | --- | --- |
| 1. Inventario | Revisar repositorios FE/BE, workflows y estado real de Oracle: revisiones desplegadas, imágenes, PostgreSQL, migraciones, volúmenes y tamaños. Identificar scripts reutilizables. | Inventario sin secretos; versiones compatibles y capacidad suficiente en destino. |
| 2. Preparación | Verificar SSD/RAM, instalar Ubuntu y actualizaciones, configurar SSH, hora, red, Docker/Compose, almacenamiento, proxy y arranque. | Identidad del host, servicios y permisos comprobados; acceso administrativo conservado. |
| 3. Automatización | Implementar instalación y traslado por etapas en fuentes versionadas, con configuración privada separada. | Revisiones y hashes identificados; pruebas en destino descartable con datos ficticios, incluidos fallos y reejecución. |
| 4. Ensayo | Generar respaldo consistente, transferirlo protegido y restaurarlo en destino aislado con las versiones correspondientes. | Base, cuentas y archivos íntegros; acceso LAN, HTTPS y pruebas funcionales. Origen continúa como instalación real. |
| 5. Recuperación | Automatizar respaldo externo, probar restauración en entorno vacío y comprobar arranque tras reinicio. Medir carga representativa. | Recuperación completa comprobada, alertas entregadas y recursos registrados. |
| 6. Corte | Acordar ventana, detener escrituras en Oracle, tomar copia final y repetir restauración/verificaciones. | Maxi acepta el destino antes de habilitar escrituras locales. Origen queda conservado y sin escrituras. |
| 7. Operación | Documentar actualización manual, mantenimiento, respaldos y recuperación. | Operador puede seguir el procedimiento; pendientes y evidencias fechados. Retirar Oracle solo por decisión expresa posterior. |

El ensayo con copia de datos reales conserva privacidad y aislamiento; desactivar
integraciones que puedan producir efectos externos. Las escrituras de prueba no
se incorporan al corte final. No se necesita copiar toda la VM ni sus herramientas
temporales: trasladar producto y datos inventariados, sin clonar configuraciones
de red, accesos o privilegios exclusivos de Oracle.

## Automatización a implementar

Separar preparación del host, respaldo/traslado, restauración y actualización.
Nombres, opciones CLI y ubicación final del código se decidirán al revisar las
fuentes de FE/BE; **no hay comandos ejecutables nuevos en este documento**.
Reutilizar mecanismos existentes cuando preserven sus garantías.

- La preparación debe comprobar requisitos, explicar cambios con privilegios y
  poder repetirse sin duplicar configuración ni reemplazar secretos o datos.
- Registrar operación, destino, revisiones, etapa y resultado sin datos privados.
  Ante fallo o interrupción, inspeccionar antes de reanudar; no marcar éxito parcial.
- Respaldar PostgreSQL mediante exportación lógica compatible y los archivos en
  el mismo punto consistente. Incluir cuentas y configuración protegida. Un dump
  solo no recupera el producto completo; no copiar un volumen PostgreSQL activo
  como si fuera un respaldo portable.
- Usar manifiesto versionado con revisiones FE/BE, versiones de base/herramientas,
  migraciones y checksums de archivos. Verificar integridad antes de restaurar.
- Restaurar primero en destino vacío y aislado. Reemplazar datos existentes exige
  confirmación explícita del destino y una copia recuperable previa.
- Separar restauración del traslado y migraciones nuevas de esquema. Primero
  recuperar la revisión de origen; cualquier actualización posterior sigue
  [migraciones-admin.md](migraciones-admin.md), con SQL y verificadores específicos.
  No reutilizar verificadores históricos que exigen tablas vacías.
- Conservar releases y respaldo anterior. No usar etiquetas `latest`, borrado de
  volúmenes ni limpieza automática para resolver errores o falta de espacio.

La utilidad existente **kume-admin** administra consultas y migraciones de esquema;
instalarla no instala KUME completo. La nueva skill coordina el traslado sin
ampliar silenciosamente los permisos de esa utilidad.

## GitHub y configuración del destino

La migración inicial puede realizarse con versiones concretas sin crear pipelines
nuevos. Para actualizaciones, revisar y adaptar los workflows FE/BE existentes:
conservar build y controles compartidos, agregando empaquetado para destino local
solo donde sea necesario. No duplicar toda la CI.

Propuesta de entrega: paquete o imagen inmutable, manifiesto con revisiones
compatibles y checksums; descarga desde el servidor y activación manual verificada.
Elegir almacenamiento y autenticación antes de implementar: los artifacts de
Actions caducan y los repositorios/registries privados requieren credenciales con
alcance mínimo. No asumir descargas anónimas, retención ilimitada o costo cero.
Guardar la versión activa y una versión recuperable en el equipo.

| Lugar | Qué configurar | Qué no trasladar por defecto |
| --- | --- | --- |
| GitHub | Configuración de empaquetado, destino lógico y permisos mínimos para publicar artefactos. Un environment `local` es una opción por concretar. | Claves SSH de acceso entrante al servidor si el método es descarga local; secretos de aplicación dentro de artefactos. |
| Servidor | Conexión PostgreSQL interna, cuentas con hashes, origen HTTPS, archivos, permisos, certificados, respaldo y credencial de lectura de artefactos si hace falta. | IP/dominio Oracle, credenciales de Actions y rutas absolutas heredadas sin revisión. |
| Navegador | Frontend compilado y origen/API configurados de forma compatible. | Contraseñas de base, token de Clock, credenciales de descarga o secretos administrativos. |

Los nombres reales de variables, archivos privados, servicios y rutas se obtendrán
de las versiones elegidas; no se fijan nombres nuevos por suposición. Trasladar
o rotar secretos de forma protegida y comprobar acceso sin publicarlos en chat,
logs o repositorio. Respaldar la configuración necesaria para recuperarlos.

Un runner de GitHub alojado no alcanza por defecto la intranet. No abrir SSH ni
agregar túneles para resolverlo. Un runner local dedicado queda como alternativa
futura, pendiente de revisar aislamiento y permisos; no es requisito inicial ni
se instalará sobre el servidor productivo por inferencia.

Al actualizar: comprobar compatibilidad FE/BE y esquema, espacio, respaldo y
ausencia de otra operación; preparar, verificar salud y activar. Si hubo cambios
de esquema, volver a una imagen anterior no implica que los datos sean compatibles.

## Red, dependencias y respaldos

Definir reserva DHCP o IP estable, nombre interno y certificados confiables para
los clientes, con renovación comprobada. Frontend y API bajo un mismo origen
HTTPS; PostgreSQL y salud internos, archivos servidos por API autorizada.
Deshabilitar suspensión y comprobar arranque tras reinicio; evaluar recuperación
de encendido en BIOS según la operación elegida. No simular un corte brusco sobre
datos reales para probar la ausencia de UPS.

Gastos, personal y autenticación deben funcionar localmente sin cloud. La futura
[integración con SoftwareClock](../technical/softwareclock-api.md) sí depende de
internet para obtener nuevas marcas: su diseño contempla conservar la última
consulta y señalar datos desactualizados ante error, según las
[reglas de horas](../functional/registro-horas.md). No prometer sincronización
offline ni integración ya implementada. Inventariar esta dependencia si el módulo
está incluido en la revisión finalmente migrada. Instalación, descarga de releases,
actualizaciones y algunos destinos de respaldo también requieren internet.

Mantener las reglas de [respaldo del alcance](../functional/alcance-prototipo.md):
copia diaria consistente y cifrada, retención de 30 días, alertas a Maxi y claves
recuperables por KUME; restauración inicial y trimestral. Elegir destino externo
al equipo y dimensionar retención, espacio temporal y crecimiento de documentos.
No multiplicar copias completas por 30 dentro del SSD sin comprobar capacidad.
Un disco conectado al servidor requiere además resolver custodia fuera del lugar
y el riesgo compartido ante robo o daño; su compra no completa la estrategia.

## Verificaciones de aceptación

- Gastos, totales, anulados, filtros/CSV, rubros, personal, asignaciones, cursos,
  talleres y funciones efectivamente incluidas en la revisión trasladada.
- Cantidades y relaciones de datos; hashes y apertura de comprobantes/documentos;
  acceso de cuentas y rechazo de operaciones/archivos sin sesión.
- HTTPS confiable desde otra computadora LAN; operación local sin cloud para las
  funciones que no dependen de proveedores externos.
- Uso representativo hasta cinco personas: consultas, cargas y exportaciones;
  medir latencia, memoria disponible, CPU y espacio sin afirmar umbrales no medidos.
- Persistencia y arranque tras reinicio controlado, cierre de sesiones esperado,
  copia externa y recuperación en entorno vacío.
- Procedimiento de vuelta atrás: antes de escrituras locales se puede rehabilitar
  origen tras verificarlo; si ya hay cambios locales, bloquear escrituras y
  transferir/reconciliar esos cambios antes de reabrir Oracle. No perderlos
  restaurando simplemente una copia vieja.

Cinco personas es el objetivo de capacidad, no autorización para crear cuentas
compartidas ni evidencia de cinco cuentas configuradas. Revisar ampliación de
cuentas individuales al implementar, conservando las reglas de autenticación.

## Esfuerzo y pendientes para retomar

Estimación preliminar conversada: **3–6 días de trabajo técnico**, no cotización
ni plazo comprometido. Preparación/automatización inicial 1–2 días; migración y
recuperación 1–2; entrega GitHub/documentación 0,5–1,5, con margen de redondeo y
ajustes. Reestimar tras inventario de workflows, volúmenes y versiones reales.
No incluye desarrollar módulos pendientes, compra, espera de equipo ni contratos
de mantenimiento. No contratar servicios ni habilitar pagos automáticamente.

- [x] Registrar camino de migración, configuración de referencia y skill interna.
- [ ] Confirmar equipo disponible, Ubuntu instalado y estado de SSD/RAM.
- [ ] Inventariar Oracle y repositorios FE/BE con evidencia actual, sin secretos.
- [ ] Concretar red/HTTPS, respaldo externo, retención y alertas.
- [ ] Elegir formato, almacenamiento y descarga de releases; fijar variables reales.
- [ ] Implementar y probar automatización y ajustes de workflows.
- [ ] Ejecutar ensayo, restauración y mediciones de capacidad.
- [ ] Acordar corte definitivo y obtener aceptación del destino.

Registrar aquí fechas, revisiones y resultados cuando cada etapa se ejecute;
mantener los resultados detallados en una memoria operativa vinculada si crecen.
