# KUME Admin — Reglas generales de interfaz

Fecha: 13 de noviembre de 2026. Fuente: acuerdos explícitos de Maxi en la sesión de revisión visual.

## Estado y alcance

**Estado: aprobado como regla general de interfaz del sistema por Maxi.** La aprobación comprende la dirección B institucional, los componentes, estados e interacciones acordados y la composición del piloto de Gastos con sus ajustes finales. Estas reglas se aplican a las pantallas actuales y futuras, respetando las reglas de negocio y recorridos propios de cada módulo.

Gastos es la referencia visual aprobada para listado, formulario y detalle; no limita el alcance del sistema visual a ese módulo. La adopción en el frontend y el plan de extensión son tareas posteriores. Esta aprobación no acredita implementación de producto, verificación completa de accesibilidad ni cierre del paso 4.

Se revisaron instrucciones y fuentes del repositorio de documentación, el frontend `maxifarkuso/kume-admin-fe` y los bocetos G01–G05 del proyecto MagicPath `467706881381666816`. El frontend fija su referencia documental a `0a4a28e36c03fa4cf0ec30f00edaf5c6b13295fd`. La revisión inicial fue de código y estilos, sin acreditar una prueba del producto desplegado.

El objetivo es claridad y rapidez para una secretaria administrativa sin conocimientos técnicos, con prioridad de escritorio. Se conservan reglas y flujos de [navegación y pantallas](screen-design.md), [alcance](../functional/alcance-prototipo.md) y [registro de pagos](../specs/003-payment-records/spec.md). Este documento es propietario de los nuevos acuerdos visuales; no duplica contratos ni sustituye sus fuentes.

## Dirección elegida

Se presentaron A, serena y cercana (verde y marfil, continuidad visual); B, precisa e institucional (azul y gris frío); C, cálida y contemporánea (petróleo y arena). La recomendación inicial fue A; Maxi eligió **B**.

Personalidad: ordenada, sobria, legible, con acciones reconocibles y decoración contenida. Densidad equilibrada. Menú lateral claro, sección activa en azul suave, texto azul oscuro y peso tipográfico destacado. Por ajuste expreso de Maxi, sin borde azul oscuro lateral y con opciones 8 px más angostas (4 px adicionales de margen por lado en la maqueta).

| Decisión | Acuerdo |
| --- | --- |
| Tipografía | `system-ui`, con alternativas locales de respaldo; sin descarga de fuentes. Verdana fue considerada, no elegida. |
| Texto y etiquetas | Texto base y etiquetas de inputs de 16 px; etiquetas con peso 600. |
| Botones y acciones de fila | Icono y texto visible de 14 px, peso 600; texto ligeramente menor que las etiquetas de campos. Área de interacción cómoda. |
| Densidad | Controles de 44 px; todos los filtros con la misma altura exacta. Filas de referencia de aproximadamente 48 px; permitir mayor altura para contenido largo. |
| Esquinas | Radio de 6 px en botones, campos y selectores. |
| Botón principal | Azul sólido. En formulario: «Guardar gasto». |
| Botón secundario | «Cancelar», junto al principal al final del formulario, alineados a la izquierda. |

### Valores del sistema visual

Estos valores concretan la dirección y la maqueta aprobadas y constituyen la base común del sistema. Las dimensiones de paneles pueden adaptarse al contenido de cada pantalla sin cambiar la jerarquía, densidad ni accesibilidad acordadas.

| Uso | Valor |
| --- | --- |
| Acción principal | `#2456A6` |
| Fondo de aplicación | `#F4F6F9` |
| Superficies y navegación | `#FFFFFF` |
| Texto principal | `#243247` |
| Texto secundario | `#526176` |
| Selección suave | `#EAF0FB` |
| Borde de controles | `#8290A3` |
| Separadores decorativos | `#DDE3EC` |
| Error | Texto `#A12632`, fondo `#FFF1F2` |
| Éxito | Texto `#236342`, fondo `#EDF7F0` |
| Advertencia/anulado | Texto `#78500D`, fondo `#FFF7E6` |
| Foco | Anillo azul visible con separación respecto del control |
| Espaciado | Escala común: 4, 8, 12, 16, 24 y 32 px |
| Títulos | 28–32 px; secundarios 18–20 px |

Iconos de trazo simple, consistentes, acompañados por texto en acciones principales y de fila. La maqueta usa SVG propios; no se aprobó incorporar ninguna librería de iconos, framework CSS ni dependencia de producción. Iconos decorativos ocultos a tecnologías de asistencia; botones de solo icono con nombre accesible.

## Aplicación transversal

Estas reglas son la fuente visual común para Gastos, Personal, Rubros, Cursos, Talleres, autenticación y nuevas pantallas autorizadas. Aplicar paleta, tipografía, tamaños de etiquetas y botones, radios, espaciado, foco y mensajes de forma consistente. Login conserva su estructura propia sin menú privado; los catálogos conservan formularios breves en diálogos y Gastos/Personal sus formularios en páginas completas según los recorridos aprobados.

- Filtros: altura uniforme de 44 px y aplicación automática cuando cambian; conservar contexto al navegar. No agregar campos de Gastos a otros módulos por analogía.
- Formularios: etiquetas permanentes, acciones principal y secundaria coherentes, errores asociados y conservación del trabajo. Usar nombres de acción propios del recurso.
- Tablas: acciones frecuentes visibles con icono y texto de 14 px, importes a la derecha y contenido largo legible. La composición destinatario/concepto de Gastos no obliga a agrupar columnas ajenas.
- Información contextual: datos principales siempre visibles; explicaciones mediante botón ⓘ activado con clic/teclado, cerrado inicialmente y descartable con Escape o clic fuera.
- Archivos: selección clara, formato/tamaño permitido visible, nombre y tamaño tras seleccionar y acción para cambiar. Cantidad, obligatoriedad y operaciones dependen del contrato de cada módulo.
- Confirmaciones, carga, vacío, error, éxito, foco y deshabilitado siguen los criterios comunes de este documento. Estados de dominio y restricciones conservan su fuente funcional.
- Importes UYU: aplicar el componente de ingreso desde centésimos y presentación decimal acordados donde se capturen importes, sin alterar precisión ni contratos.

Los ejemplos de textos y filtros de las secciones siguientes concretan estas reglas en Gastos. No crean operaciones ni estados funcionales en otras áreas. El cabezal «Revisión visual» y los selectores Pantalla/Estado son herramientas exclusivas de la maqueta y quedan fuera de la UI de producto.

## Componentes y comportamiento acordados

### Navegación y filtros

Se conservan los cinco destinos permanentes y la separación entre Trabajo diario y Administración. La entrada normal sigue siendo Gastos del mes actual, sin dashboard adicional.

En Gastos: Mes, Rubro y Estado agrupados; «Período personalizado» muestra Desde y Hasta. Los filtros se aplican automáticamente al cambiarlos, sin botón Aplicar; no cambia el comportamiento actual. Conservar filtros y página al volver de alta/edición. Exportar CSV usa el mismo conjunto filtrado, sin limitarse a la página.

### Total e información contextual

El total está **siempre visible**, acompañado por un botón de información `ⓘ`. La tarjeta explicativa está cerrada inicialmente y aparece únicamente al activar ese botón, nunca por hover o por recibir foco. Texto: «Suma todos los gastos del filtro actual, de todas las páginas. Excluye los gastos anulados».

Cerrar mediante otra activación, clic fuera o Escape. El botón funciona también con Enter/Espacio, tiene nombre accesible y comunica expansión. Escape devuelve el foco al botón. La tarjeta no oculta el total. Su apariencia sigue la maqueta aprobada y debe adaptarse para no quedar fuera del área visible.

### Tabla y acciones

Importes alineados a la derecha, dos decimales y cifras tabulares. Mantener fechas legibles y acciones visibles por fila: «Ver detalle» con icono de documento y «Comprobante ↗». Texto de 14 px; no reemplazarlas por iconos solos ni ocultarlas en un menú. La apertura del comprobante sigue siendo en otra pestaña y se indica en el nombre accesible. Mantener paginación y total independiente de la página.

### Formulario e importe

Formulario en página completa, con etiquetas permanentes y grupos Datos del gasto y Comprobante. «Guardar gasto» principal y «Cancelar» secundario al final, alineados a la izquierda.

El ingreso del importe parte de los **centésimos**:

| Acción | Resultado visible |
| --- | --- |
| Escribir `1` | `0,01` |
| Escribir `132050` | `1320,50` |
| Retroceso sobre `1320,50` | `132,05` |
| Seleccionar todo y escribir | Reemplaza el importe anterior |
| Pegar `1320,50` | `1320,50` |
| Pegar `1320.50` | `1320,50` |
| Pegar `132050` | `1320,50` |

Mostrar moneda UYU y ayuda: «Ingresá los números sin coma; los últimos dos son centésimos». No modificar el contrato: el importe sigue viajando como texto decimal exacto y siendo positivo. Evitar punto flotante para cálculos contables. No interpretar silenciosamente pegados ambiguos o inválidos. Quedan por concretar antes de implementar los pegados con miles/moneda, selección parcial, Delete y límites de edición; la maqueta no los convierte en acuerdos.

Comprobante: bloque con «Seleccionar archivo», indicación «PDF, JPG o PNG · Hasta 10 MB» y, una vez elegido, nombre, tamaño y acción «Cambiar archivo». Se conservan archivo único obligatorio y validaciones canónicas. En edición se consulta el actual; el reemplazo es una acción independiente del detalle.

### Detalle y diálogos

Detalle en dos columnas: datos a la izquierda; comprobante a la derecha con nombre, formato, tamaño y acciones Ver, Descargar y Reemplazar. Se conserva apertura en otra pestaña y reemplazo con confirmación, sin historial.

Confirmaciones de anulación, restauración y reemplazo en diálogos centrados. Explicar consecuencias, identificar el gasto/archivo y usar verbos concretos («Volver», «Anular gasto», etc.). Foco inicial en opción menos riesgosa, navegación contenida en el diálogo y devolución al control de origen al cerrar. El aviso de salida con cambios sin guardar de G05 se conserva.

## Estados acordados

| Estado | Presentación y respuesta |
| --- | --- |
| Carga | Filas de espera discretas, sin animaciones intensas; «Cargando total…», sin mostrar cero o el total anterior como vigente. |
| Guardado | «Guardando…», impedir doble envío; no anunciar éxito antes de confirmar respuesta. |
| Primer uso | «Todavía no registraste gastos», con «Registrar gasto». |
| Filtros sin resultados | «No hay gastos para estos filtros», con «Restablecer filtros»; el restablecimiento conserva el criterio aprobado de volver al mes actual. |
| Error de campo | Mensaje junto al campo, datos conservados y foco en el primer error al intentar guardar. |
| Error de consulta/servicio | Mensaje comprensible y reintento manual; conservar filtros y no presentar datos anteriores como actuales. |
| Éxito | Aviso dentro de la página, cerca del título, persistente y cerrable; dura hasta cerrarlo o cambiar de pantalla. Ejemplo «Gasto guardado · Ver gasto». |
| Anulado | Etiqueta «Anulado» y aviso «Este gasto no suma en los totales. Restauralo para editarlo». Solo consulta y descarga hasta restaurar. |
| Foco | Siempre visible, sin depender solamente de color; orden lógico de teclado. |
| Deshabilitado | Diferenciable de habilitado, conservar legibilidad y explicar indisponibilidad cuando corresponda. No usar cursor de espera salvo procesamiento. |
| Conflicto de versión | Conservar trabajo y explicar cómo recargar sin sobrescribir silenciosamente. Se conserva la política existente. |

## Accesibilidad y consistencia

Objetivo de accesibilidad: WCAG 2.2 AA. Verificar contraste de texto normal de al menos 4,5:1 y de controles/foco relevantes de al menos 3:1; no afirmar conformidad total por elegir una paleta. Etiquetas asociadas, ayudas y errores vinculados, `aria-invalid`, estructura semántica de tablas y anuncios de carga/éxito sin mover foco innecesariamente. Los errores requieren texto, no solo rojo. Mantener zoom, texto largo, teclado completo y preferencia de movimiento reducido. La fuente puede variar por sistema operativo: revisar Windows, macOS y Linux durante implementación.

Usar los mismos componentes y estados en todas las pantallas; Gastos es el piloto visual aprobado para su adopción progresiva. No introducir dependencias de producción sin conversarlo.

## Maqueta y próximo paso

Se autorizó preparar una maqueta visual de listado/filtros, formulario y detalle con datos ficticios, incluyendo estados acordados. Se reutiliza MagicPath, proyecto `467706881381666816`, sin reemplazar G01–G05. La maqueta es una demostración local sin API, sesiones, persistencia ni manejo de archivos de producción; sus interacciones no acreditan implementación funcional ni pruebas integradas.

La maqueta creada, sus capturas, revisión de MagicPath y evidencia de verificación están en [Maqueta visual de Gastos](maquetas/gastos/README.md). La aprobación visual fue dada expresamente por Maxi; la compilación y comprobación local solo acreditan la maqueta, no la implementación del producto.

La composición y los componentes están acordados. El siguiente paso es preparar el plan de implementación y extensión. Maxi autorizó subir los acuerdos a `kume-admin-docs` como reglas generales del sistema; esa autorización comprende commit y push documental, no implementación del frontend, merge de código, despliegue ni cierre del paso 4.

## Revisión de la maqueta — ajustes aprobados

Maxi indicó que el resto del diseño está perfecto y solicitó quitar el borde azul oscuro izquierdo de la opción seleccionada y achicar unos píxeles el ancho de las opciones del menú. Se conserva fondo azul suave y texto destacado para la selección; la reducción aplicada en la maqueta es de 8 px totales por opción.

El cabezal «Revisión visual», el selector Pantalla y el selector Estado son herramientas exclusivas de la maqueta. Tras aclararlo, Maxi pidió expresamente **conservarlos**. No forman parte de la UI final ni se incorporan al frontend. Estado permite revisar carga, vacío, error y éxito; Pantalla permite alternar listado, formulario y detalle para revisión. No se acordó cambiar por breadcrumbs ni quitar estos controles de revisión.

La aprobación inicial del piloto fue ampliada por Maxi a reglas generales de interfaz del sistema. No completa el paso 4 general ni aprueba implementación, backlog, dependencias o despliegue. La revisión de las dimensiones exactas del ajuste lateral no reabre el resto del diseño aprobado.

### Ajuste final de filtros

Maxi aprobó el ajuste del menú y solicitó que todos los campos de filtros tengan el mismo alto. Se fija una altura uniforme de **44 px** para mes, fechas Desde/Hasta y selectores de período, rubro y estado, con el mismo modelo de caja y centrado vertical. Se conserva el comportamiento automático de los filtros.
