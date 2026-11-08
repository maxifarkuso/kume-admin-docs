# Registro de pagos — implementación local y evidencia

Fecha: 8 de noviembre de 2026. Backend y frontend en `feat/payment-records`; documentación en `main`. Sin commits, push, PR, merge ni despliegue.

## Resultado revisable

Backend: módulos `expenses` y `categories`, dominio de dinero/fechas, aplicación con puertos, persistencia Prisma y rutas protegidas por la autenticación existente. Quince operaciones de gastos/rubros. Versionado atómico de cada escritura y reemplazo, bloqueo coordinado del rubro, fechas de negocio America/Montevideo y totales decimales exactos.

Comprobantes privados mediante @fastify/multipart 10.1.8: límite en streaming, extensión/MIME/firma, claves opacas, compensación de archivos nuevos al fallar y limpieza del anterior solo tras éxito. Los errores de limpieza quedan identificados para recuperación. La creación acepta el campo JSON `data` separado del archivo `receipt`; el navegador lo envía como parte application/json y el parser limita también el tamaño de esos metadatos.

Frontend: listado con mes/fechas, rubro y estado, paginación, total, CSV, alta/edición en páginas completas, detalle, consulta/descarga, reemplazo confirmado y anulación/restauración. Administración de rubros con creación, edición y estados. Tras guardar vuelve al listado conservando contexto y ofrece «Ver gasto». Los formularios conservan la versión inicial y el borrador ante conflicto; el reemplazo conserva la versión al seleccionar el archivo.

Migración aditiva `20261108170000_payment_records`: tablas, checks, índices, claves foráneas restrictivas, timestamps y rubros iniciales. Se preparó, **no se aplicó**. Compose exige directorio persistente privado y configura FILES_ROOT; no se ejecutó Compose ni se cambió producción.

## Comprobaciones ejecutadas

| Área                | Resultado                                                                                                                                                                                                                                   |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Backend, unitarias  | 65 pruebas en 12 archivos correctas. Incluyen dinero/fechas, CSV, compensaciones, reemplazo y validación de archivos con directorios temporales ficticios.                                                                                  |
| Frontend, unitarias | 32 pruebas en 7 archivos correctas. Incluyen formulario/comprobante, fecha de negocio, versión en acciones y conservación de borrador/versión frente a actualización y 409.                                                                 |
| Ambos, lint         | Correcto, incluidos límites de dependencias; frontend también Stylelint.                                                                                                                                                                    |
| Ambos, tipos/build  | Compilación completa correcta; backend genera cliente Prisma con herramientas oficiales y frontend compila con Vite.                                                                                                                        |
| Contrato local      | OpenAPI validado; 15 rutas y cuerpos JSON contrastados por inspección de metadatos, respuestas generadas y DTO de ambos consumidores verificados contra el archivo canónico local.                                                          |
| Arranque de rutas   | createApp/ready compila rutas, parser y esquemas sin ejecutar peticiones ni conectar PostgreSQL.                                                                                                                                            |
| Referencia fijada   | **contract:check ordinario falla en ambos consumidores**: los DTO nuevos difieren del snapshot anterior fijado a 1e650636705371f09be51a8c77a67f39e5251ba3. No se alteró ese snapshot ni se afirmó que su commit contiene el contrato nuevo. |

Contrato local aprobado, SHA-256: `1e0a56671f98962fca99c3f77292ade48cbc42c59a9bb82bf8adc83cc04f8f85`. Este digest identifica el archivo probado; no sustituye un commit canónico.

## Reproducir la revisión local

Con dependencias instaladas y desde backend:

```sh
node --import tsx scripts/contract.mjs --contract /workspace/kume-admin-docs/openapi.yaml
node --import tsx scripts/payment-contract.mjs --contract /workspace/kume-admin-docs/openapi.yaml
```

Desde frontend:

```sh
node scripts/check-generated.mjs --contract /workspace/kume-admin-docs/openapi.yaml
```

`--contract` permite una revisión explícita sin cambiar el snapshot fijado. El chequeo ordinario conserva sus exigencias; estos comandos locales no acreditan sincronización ni CI remota.

## Pendientes y límites

Antes de publicar: autorizar e incorporar el contrato a un commit de docs, sincronizar referencias/hashes de ambos consumidores, regenerar y obtener contract:check ordinario correcto. Coordinar despliegue del cambio incompatible.

Antes del despliegue: revisar/aplicar migración conforme la instrucción previa de Maxi; preparar KUME_RECEIPTS_DIR con escritura para el usuario node del contenedor, configurar volumen privado e incluirlo en respaldos junto con PostgreSQL. No mantener comprobantes en el filesystem efímero de la imagen.

No se probaron SQL, migración/reaplicación, carreras PostgreSQL, proxy, navegador integrado, cargas HTTP multipart ejecutadas ni restauración real. Las unitarias y compilación de rutas no sustituyen estas comprobaciones. No se instaló Playwright ni se introdujo una suite de integración no acordada. Revisar el tratamiento de fórmulas al abrir CSV en planillas según el pendiente técnico; la exportación actual conserva los textos con escape RFC4180.

Riesgo alto por persistencia, dinero, concurrencia y archivos privados. No habilitar piloto real a partir de esta evidencia local. El paso 4 de pantallas conserva su estado.

## Reversión

Retirar rutas/pantallas de esta feature o volver al artefacto anterior compatible; conservar tablas y archivos, sin migración down destructiva. Si se aplicaron escrituras nuevas, no operar dos versiones en paralelo y comprobar compatibilidad antes de reabrir escritura. Conservar respaldo consistente antes de migraciones y mantenimiento.
