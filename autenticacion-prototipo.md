# KUME — Autenticación del prototipo

**Fecha:** 2 de noviembre de 2026
**Estado:** alcance confirmado explícitamente por Maxi mediante GrillMe. Diseño técnico y contrato completos; decisiones de cambio de contraseña y pausas confirmadas por Maxi. Implementación, pantallas, despliegue y verificación pendientes.

## Decisiones confirmadas

- Dos cuentas individuales: Maxi (técnico) y Vicky (secretaria), con los mismos permisos completos sobre los datos.
- Credenciales en un archivo de secrets del servidor, con hashes de contraseña, sin tabla de usuarios. No guardar contraseñas en texto plano ni exponer secrets al navegador, al repositorio o a los logs.
- Acceso por Internet con HTTPS. Las pantallas privadas y todas las operaciones de negocio, CSV y archivos requieren sesión válida; el backend aplica la protección aunque se acceda directamente a una URL.
- Cierre manual de sesión y vencimiento tras 8 horas de inactividad.
- Cambios de contraseña manuales en secrets, a cargo de Maxi.
- Límite de intentos por cuenta y por dirección IP, con pausas temporales y sin bloqueo permanente.
- Sin registro público, recuperación por correo, pantalla de administración de usuarios ni permisos diferenciados.
- Mantener separación entre demo y piloto real, incluyendo credenciales, datos y archivos, según el alcance existente.

Este acuerdo sustituye los requisitos previos de recuperación por correo y de modelar usuarios en base de datos. Las fichas del personal continúan siendo entidades de negocio independientes de las cuentas de acceso.

## Sesiones y alojamiento — decisiones confirmadas el 2 de noviembre

### Alojamiento

- Frontend compilado y API bajo un mismo origen HTTPS en la VM Oracle: el proxy sirve React y reenvía `/api/v1/...` a Fastify. Esto sustituye la alternativa inicial de Cloudflare Pages.
- El puerto de Fastify no se publica directamente a Internet. `/health` se usa dentro de la red de contenedores; el proxy público no publica esa ruta. Si se sirven Swagger y `/openapi.json`, el proxy los dirige también a Fastify para aplicar su autenticación; no copiarlos como archivos públicos ni dejar que el fallback de React los sustituya.
- Un origen por entorno, configurado explícitamente; demo y piloto separados. Dominio, certificados y configuración concreta del proxy siguen pendientes de despliegue.
- En desarrollo, Vite reenvía `/api` al backend para conservar el mismo origen. La excepción de HTTP y cookie sin `Secure` solo corresponde a desarrollo local, con nombre distinto (`kume_session_dev`); no usarla en demo o piloto.

### Sesión en memoria

- Una instancia y un proceso Fastify por entorno. Sesiones en memoria del backend, sin tablas de usuarios o sesiones ni servicio adicional.
- Identificador opaco generado con 32 bytes aleatorios criptográficos, codificado en base64url. El servidor guarda su hash SHA-256, el identificador de usuario y los instantes de creación y última actividad. El token no contiene credenciales ni se devuelve en JSON.
- Cookie de producción: `__Host-kume_session`, `Secure`, `HttpOnly`, `SameSite=Strict`, `Path=/`, sin `Domain` y sin persistencia mediante `Expires` o `Max-Age`. El navegador puede restaurar cookies de sesión: la caducidad efectiva se valida siempre en el servidor.
- Cada petición autenticada aceptada actualiza la última actividad, excepto `GET /api/v1/auth/session`. El polling de sesión no mantiene el acceso abierto. Tampoco lo hacen los archivos estáticos ni una pestaña simplemente abierta. No crear heartbeats automáticos que renueven la sesión.
- A las 8 horas desde la última actividad, la sesión es inválida antes de ejecutar la operación: devolver `401`, eliminarla y limpiar la cookie. Eliminar periódicamente sesiones vencidas; la comprobación por petición es obligatoria aunque la limpieza aún no haya corrido.
- Login correcto genera un token nuevo y elimina la sesión anterior presentada por ese navegador. No aceptar identificadores elegidos por el cliente. Dos computadoras pueden mantener sesiones independientes.
- Logout elimina la sesión del servidor y limpia la cookie; no basta con borrarla en el frontend. Su respuesta es idempotente aun si la sesión ya no existe.
- Reinicio, despliegue o restauración del backend elimina todas las sesiones y exige nuevo login. No respaldar ni restaurar sesiones. Escalar a varios procesos requeriría revisar este diseño.
- Las respuestas de autenticación y de datos privados usan `Cache-Control: no-store`; el proxy no almacena respuestas privadas.

### Protección de solicitudes

- Autenticación obligatoria por defecto en el backend: datos, CSV, cargas y descargas. Swagger y el contrato servido también requieren sesión; los documentos descargados del repositorio no son un servicio público.
- Excepciones explícitas: login; logout idempotente; `/health` solo en red interna. Los recursos estáticos y la pantalla de login no contienen datos privados; la API es la autoridad de acceso.
- Todas las escrituras, incluido login y logout, exigen `Origin` igual al origen configurado y la cabecera `X-Kume-Request: 1`. Rechazar origen ausente, `null` o distinto, y cabecera ausente o inválida, con `403`. El frontend agrega esta cabecera también a multipart; no fija manualmente su `Content-Type`.
- Cookie `SameSite=Strict`, cabecera no simple y validación de origen conforman la protección CSRF. Ningún GET modifica datos de negocio. No habilitar CORS para orígenes externos ni reflejar el origen recibido. El proxy conserva `Origin` y no agrega la cabecera requerida en nombre del cliente.
- Solo confiar en cabeceras de IP reenviadas por el proxy configurado explícitamente; este debe reemplazar las aportadas por Internet. No usar confianza indiscriminada en `X-Forwarded-For`.

### Contrato HTTP

| Método | Ruta | Resultado |
|---|---|---|
| POST | `/api/v1/auth/login` | Recibe `username` y `password`, crea sesión y entrega cookie; `200` con usuario y `expiresAt` |
| GET | `/api/v1/auth/session` | Consulta usuario y vencimiento actual sin renovar actividad; `200` o `401` |
| POST | `/api/v1/auth/logout` | Invalida la sesión presentada y limpia cookie; `204`, incluso si ya no existe |

`expiresAt` es el vencimiento calculado al responder, no una duración fija desde el login. `username` se normaliza quitando espacios exteriores y pasando a minúsculas; la contraseña no se recorta ni normaliza. Los identificadores del piloto son `maxi` y `vicky`; no se requiere correo.

Errores con el formato `Problem` existente: `401 INVALID_CREDENTIALS` para login fallido, `401 SESSION_REQUIRED` para sesión ausente, inválida o vencida; `403 REQUEST_ORIGIN_REJECTED` o `REQUEST_HEADER_REQUIRED` para protección de solicitudes; `429 LOGIN_RATE_LIMITED` con `Retry-After` en segundos. Credenciales incorrectas tienen el mismo mensaje exista o no el usuario. No revelar el motivo concreto de verificación de contraseña.

El frontend consulta sesión al entrar en una ruta privada. Ante `401`, limpia datos privados visibles y vuelve al login con un mensaje comprensible. No reenvía automáticamente una escritura tras autenticarse. Al cerrar sesión descarta los datos privados en memoria y evita reutilizarlos al navegar atrás.

## Credenciales y operación — diseño técnico

### Hash y formato de secrets

- Usar `scrypt` asíncrono de `node:crypto`: `N=32768`, `r=8`, `p=3`, `maxmem=67108864` bytes; salt aleatorio de 16 bytes por contraseña y clave derivada de 64 bytes. Comparar claves de igual longitud mediante `timingSafeEqual`. No usar SHA-256 solo para contraseñas: el SHA-256 de sesión tiene otro propósito.
- Estos parámetros definen el diseño inicial, no una medición de rendimiento. Verificar compatibilidad con la versión de Node elegida y medir latencia y memoria en la VM antes del piloto; no reducir parámetros silenciosamente para resolver problemas de carga. No bloquear el event loop ni lanzar verificaciones sin un límite de concurrencia.
- Archivo JSON, versión 1, con `users`: cada entrada incluye `username`, `displayName` y `passwordHash`. Este último contiene `algorithm` (`scrypt`), `N`, `r`, `p`, `salt` y `derivedKey`; los dos últimos son base64 estándar. Validar tamaños decodificados, parámetros exactos, versión, campos y unicidad de usuarios antes de aceptar tráfico. `maxmem` es un límite del código, no un valor suministrado por el cliente.
- El piloto contiene únicamente `maxi` y `vicky`, con hashes y salts independientes y los mismos permisos definidos por la aplicación. La demo tiene su propio archivo y contraseñas; no copiar las credenciales reales.
- Configurar `AUTH_USERS_FILE` para localizar el archivo, montado solo lectura en el contenedor. Una ruta interna como `/run/secrets/kume-auth-users.json` es referencia de montaje; la ruta del host es configurable y no se incorpora al código.
- Solo el usuario de despliegue y la identidad que ejecuta la API pueden leerlo: usar permisos `0400` o `0600` según la propiedad y el método de montaje. Verificar permisos efectivos dentro y fuera del contenedor; excluir archivo, temporales e históricos del repositorio, contexto de construcción e imagen.
- Cargar y validar una vez al iniciar. Archivo ausente, ilegible o inválido impide iniciar la API, sin cuentas por defecto, contraseñas de respaldo ni autenticación desactivada. Los errores no muestran el contenido del archivo.
- El generador administrativo pendiente debe solicitar contraseña por entrada oculta y repetirla para evitar errores. No recibirla como argumento de shell, escribirla en logs ni crear un archivo temporal en texto plano. El verificador HTTP mantiene el límite de 1024 caracteres y no trunca ni normaliza la contraseña.
- Para usuario inexistente, ejecutar una verificación ficticia con el mismo coste y devolver el mismo `401 INVALID_CREDENTIALS`. Comprobar límites de intentos antes del hash y usar comparación constante donde corresponda; ningún mensaje revela cuál campo falló.

### Cambio manual de contraseña y recuperación de acceso

Procedimiento confirmado: actualizar secrets y reiniciar el backend; se cierran **todas** las sesiones, incluidas las del otro usuario.

1. Maxi avisa del breve reinicio. Trabaja desde acceso administrativo al servidor, sin necesitar conocer la contraseña anterior de la aplicación.
2. Genera salt y hash nuevos con la herramienta administrativa pendiente, conservando la otra cuenta sin cambios. Valida el archivo completo antes de sustituirlo. No editar hashes a mano ni versionar secrets en Git.
3. Escribe el archivo nuevo con permisos restringidos y lo reemplaza de forma atómica desde el mismo filesystem. Si el montaje fija el archivo anterior, recrea el contenedor backend para garantizar que lee el archivo nuevo; no basta con reiniciar el proceso sin verificar el montaje.
4. Recrea o reinicia el backend según el montaje, comprueba arranque y salud, y verifica login con la contraseña nueva. La anterior debe fallar y todas las cookies de sesiones previas deben devolver `401`. La otra cuenta conserva su contraseña y puede volver a ingresar.
5. Si falla la validación previa, no sustituye el archivo. Si la API no arranca tras aplicar el cambio, corrige el archivo desde acceso administrativo; no abre el sistema sin autenticación. Si se pierde una contraseña, el mismo procedimiento permite asignar una nueva, sin correo.
6. Comunica la contraseña mediante un canal privado acordado, fuera de repositorio y logs, y renueva la copia cifrada de configuración para evitar depender de una copia con credenciales anteriores. La operación no se da por completada hasta comprobar acceso.

### Respaldo y traslado

- Incluir archivo de usuarios y configuración de origen en el respaldo cifrado institucional. No incluir sesiones ni contadores temporales de intentos. Custodiar las claves de descifrado separadamente y mantener acceso administrativo recuperable por KUME.
- Un dump de PostgreSQL y el volumen documental no contienen las credenciales: verificar la presencia del archivo de usuarios en la copia sin imprimirlo ni registrar hashes.
- Al restaurar o migrar, montar el archivo solo lectura, validar permisos y configuración del origen HTTPS del destino y arrancar sin sesiones previas. Comprobar acceso de ambas cuentas y aislamiento de demo.
- Restaurar una copia antigua puede recuperar contraseñas antiguas. Tras una recuperación, regenerar las contraseñas que se hayan cambiado desde la copia antes de habilitar el acceso real. La prueba de restauración sigue pendiente.

## Límite de intentos — decisión confirmada

| Dimensión independiente | Umbral en ventana móvil de 15 minutos | Pausa |
|---|---|---|
| Cuenta normalizada | 5 fallos, aunque provengan de distintas IP | 15 minutos |
| Dirección IP de cliente validada por el proxy | 20 fallos, aunque cambie el usuario intentado | 15 minutos |

- Aplicar ambos límites; basta que uno esté en pausa para rechazar el login. Una IP compartida no mezcla las cuentas para el límite de 5, pero sí acumula los fallos de ambas para el límite de 20.
- Contar verificaciones de credenciales incorrectas; entradas inválidas y solicitudes rechazadas por protección de origen/cabecera no ejecutan hash ni suman fallos de credenciales. El límite general de solicitudes y tamaño del cuerpo se configura al implementar para proteger esos casos.
- El fallo que alcanza un umbral inicia la pausa y devuelve `429 LOGIN_RATE_LIMITED`; los fallos anteriores devuelven `401 INVALID_CREDENTIALS`. Mientras haya pausa, no verificar la contraseña ni extender el bloqueo por cada petición rechazada.
- `Retry-After` indica, redondeado hacia arriba y con mínimo 1, los segundos restantes de la pausa. Si ambas dimensiones están bloqueadas, indicar la mayor espera. No informar al cliente qué dimensión activó la pausa ni si existe la cuenta.
- Un login correcto no borra fallos recientes; salen al cumplir su ventana. Al terminar una pausa se reinicia el historial de esa dimensión. Admitir inmediatamente un nuevo intento, sujeto al otro límite independiente.
- Actualizar contadores y comprobar el umbral de forma coordinada ante solicitudes concurrentes; no permitir que un lote paralelo omita la pausa. Contadores en memoria de la única instancia, con eliminación de entradas vencidas y límites de memoria definidos y comprobados durante la implementación; no registrar contraseñas ni tokens.
- Aplicar un comportamiento equivalente a nombres inexistentes para no revelar cuentas mediante tiempos o bloqueos. Normalizar nombres antes de contarlos y usar la IP validada según la política de proxy ya definida.
- Reiniciar el backend también borra contadores y pausas. Es una limitación aceptada del almacenamiento en memoria para este prototipo; no agregar persistencia ni desbloqueos remotos en esta versión. El cambio de contraseña con reinicio permite recuperar acceso administrativo a la aplicación.

## Tareas adicionales

Los pasos 2 y 3 del alcance permanecen completados por el trabajo funcional del 30 de octubre. Esta ampliación no los reabre. Las casillas de diseño y documentación completadas acreditan decisiones escritas, no seguridad implementada. Las tareas de código, pantallas, despliegue y pruebas siguen pendientes.

### Diseño técnico y contrato

- [x] Definir endpoints de login, consulta de sesión y logout; transporte y almacenamiento de sesión, invalidación efectiva y renovación por actividad. Resuelto en las secciones de sesiones y contrato HTTP; pendiente de implementación.
- [x] Definir hash y parámetros, formato del archivo de secrets, permisos de lectura, carga y procedimiento de cambio de contraseña, incluyendo el tratamiento de las sesiones existentes.
- [x] Definir umbrales, ventanas y duración de las pausas por cuenta y por IP; considerar proxy de confianza y evitar revelar si existe una cuenta.
- [x] Definir protección CSRF cuando corresponda, orígenes permitidos y configuración HTTPS compatible con el alojamiento final del frontend.
- [x] Ampliar API y OpenAPI con esquema de seguridad, excepciones públicas explícitas y errores 401/403/429. Conservar rutas y reglas funcionales aprobadas.

### Frontend y pantallas

- [ ] Diseñar login, acceso protegido, cierre manual, sesión expirada, credenciales incorrectas e intentos temporalmente limitados.
- [ ] Indicar contacto con Maxi ante necesidad de cambiar contraseña; no agregar recuperación por correo ni administración de usuarios.
- [ ] Incorporar los flujos al paso 4 conservando los bocetos de gastos y personal aprobados. El paso 4 sigue en curso y requiere su propia aprobación final.

### Backend

- [ ] Implementar herramienta administrativa de generación y validación de secrets sin exponer contraseñas.
- [ ] Validar credenciales desde secrets y crear sesiones para las dos cuentas con los mismos permisos.
- [ ] Proteger todas las operaciones de negocio, exportaciones y descargas; rechazar sesiones ausentes, vencidas o cerradas.
- [ ] Implementar vencimiento por inactividad y logout efectivo en el servidor.
- [ ] Aplicar pausas temporales por cuenta y por IP, sin registrar contraseñas ni tokens.

### Infraestructura y operación

- [ ] Configurar HTTPS y distribución protegida de secrets, con credenciales aisladas para demo y piloto.
- [x] Documentar cambio manual de contraseñas y recuperación de acceso, respaldo cifrado y traslado seguro de secrets a intranet.
- [ ] Verificar que respaldar PostgreSQL y documentos no omita la configuración necesaria para recuperar el acceso.

## Revisión de cierre — 2 de noviembre de 2026

### Balance de las tareas existentes

| Bloque | Hechas | Pendientes | Evidencia y alcance del cierre |
|---|---:|---:|---|
| Diseño técnico y contrato | 5 | 0 | Decisiones detalladas en este documento y contrato en OpenAPI; comprobación estructural del YAML y de referencias |
| Frontend y pantallas | 0 | 3 | No hay bocetos de autenticación aprobados ni integración frontend verificada |
| Backend | 0 | 5 | Herramienta administrativa, validación, protección, sesiones y límites aún sin evidencia de implementación y pruebas |
| Infraestructura y operación | 1 | 2 | Procedimiento escrito; configuración HTTPS/secrets y restauración real aún sin verificar |
| **Total de tareas** | **6** | **10** | **Diseño documentado no equivale a autenticación operativa** |

El balance se basa en el repositorio de documentación y la evidencia registrada del proyecto. No certifica el estado actual de repositorios remotos de código ni de la VM. La API temporal de prueba del 1 de noviembre no acredita estas tareas del producto.

### Qué falta para cerrar cada pendiente

| Tarea pendiente | Evidencia necesaria para marcarla hecha |
|---|---|
| Diseñar login y sus estados | Bocetos revisados y aprobados: login, cierre, sesión expirada, credenciales incorrectas, pausa temporal y acceso protegido |
| Indicar contacto con Maxi | Texto visible incorporado y revisado en el diseño de login; sin enlaces de recuperación por correo |
| Incorporar los flujos al paso 4 | Integración en el prototipo y documentación final de pantallas, conservando gastos/personal aprobados; aceptación explícita del paso 4 y backlog |
| Herramienta administrativa | Comando implementado y probado con entrada oculta, validación de archivo, salt/hash nuevos y ausencia de secretos en argumentos o logs |
| Credenciales y creación de sesión | Pruebas de ambas cuentas, mismo acceso, contraseña incorrecta, usuario inexistente, rotación del token y fallo de arranque con secrets inválidos |
| Proteger operaciones y archivos | Pruebas de acceso directo a todas las rutas protegidas: datos, CSV, descargas, cargas, contrato servido y Swagger; rechazar sesión ausente o inválida y escrituras sin protección de origen/cabecera |
| Vencimiento y logout | Pruebas con reloj controlado de 8 horas de inactividad, renovación por actividad, polling sin renovación, logout idempotente y pérdida de sesión tras reinicio |
| Pausas por cuenta y por IP | Pruebas de umbrales 5/20, ventana y pausa de 15 minutos, límites independientes/combinados, concurrencia, IP de proxy confiable, Retry-After y ausencia de extensión de pausa |
| HTTPS y distribución de secrets | Configuración desplegada y comprobada: origen único, certificado válido, cookie segura, puertos privados, secrets solo lectura, demo/piloto aislados y cambio de contraseña con reinicio verificado |
| Recuperación desde respaldo | Copia cifrada que incluya secrets/configuración, restauración en entorno vacío y acceso de ambas cuentas comprobado; sin sesiones restauradas ni pérdida del aislamiento demo/piloto |

### Condición para retomar pantallas

No quedan decisiones de autenticación pendientes para el diseño de pantallas: el contrato y los comportamientos necesarios están documentados. Las pantallas siguen pausadas en esta revisión por pedido de Maxi. Cuando se retomen, se trabajará sobre las tres tareas de frontend; el cierre completo de autenticación ocurrirá después de implementar y verificar backend e infraestructura, según el orden de trabajo acordado del proyecto.

Si el objetivo es marcar **todas** las tareas como hechas antes de continuar pantallas, no puede lograrse con documentación: tres tareas son precisamente de pantallas y otras siete requieren código o comprobaciones operativas. El balance conserva esas diez casillas abiertas y los pasos 2 y 3 completados; el paso 4 continúa en curso.

### Comprobaciones de esta revisión

- YAML analizado con detección de claves duplicadas y referencias internas resueltas; identificadores de operación únicos.
- Seguridad por defecto y excepciones explícitas cotejadas con el diseño, incluidas cabeceras requeridas en escrituras.
- Rutas, cuerpos, parámetros funcionales y respuestas de negocio previos conservados; cambios de seguridad adicionales identificados.
- Enlaces locales, estados de tareas y coherencia entre alcance, stack, API, base, infraestructura y memoria de pantallas comprobados.
- No se ejecutaron pruebas del producto ni se verificó Oracle. Los criterios siguientes permanecen pendientes hasta que exista evidencia de ejecución.

## Aceptación antes del piloto

- [ ] Maxi y Vicky pueden iniciar sesiones independientes y trabajar con los mismos permisos.
- [ ] Sin sesión válida no se accede a datos, operaciones, CSV ni archivos, incluso mediante una petición directa a la API.
- [ ] Reiniciar el backend exige nuevo login en ambas cuentas; ninguna sesión se restaura desde un respaldo.
- [ ] Un sondeo de sesión o una pestaña abierta no renuevan actividad; una operación autenticada aceptada sí.
- [ ] Las escrituras, incluido multipart, login y logout, rechazan origen o cabecera inválidos; no se accede directamente al puerto de Fastify desde Internet.
- [ ] El cierre manual invalida la sesión; tras 8 horas sin actividad se requiere volver a iniciar sesión. La verificación debe distinguir inactividad de duración total de sesión.
- [ ] Comprobar límites por cuenta e IP de forma independiente y combinada, umbrales exactos de 5/20 fallos, ventana y pausa de 15 minutos, concurrencia, vencimiento y Retry-After. Una solicitud durante la pausa no la prolonga; usuario inexistente recibe comportamiento equivalente.
- [ ] Cambiar una contraseña y reiniciar invalida todas las sesiones; la contraseña anterior falla, la nueva funciona y la otra cuenta conserva sus credenciales. Probar el montaje efectivo tras reemplazo atómico del archivo.
- [ ] Archivo de secrets ausente o inválido impide el arranque. Medir el coste de scrypt y limitar verificaciones concurrentes antes de habilitar datos reales.
- [ ] No se exponen credenciales, hashes ni tokens en respuestas o logs. El despliegue real usa HTTPS.
- [ ] La restauración recupera el acceso y mantiene el aislamiento entre demo y piloto.

Referencias: [alcance](alcance-prototipo.md), [API](api-design.md), [base de datos](database-design.md), [OpenAPI](openapi.yaml), [infraestructura](infraestructura-y-migracion.md) y [continuación de pantallas](continuacion-diseno-pantallas.md).
