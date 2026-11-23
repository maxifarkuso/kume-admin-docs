# CU0 — Configuración y rotación de secrets

**Procedimiento propuesto para la futura implementación.** El backend actual usa un archivo privado de usuarios de KUME montado en solo lectura. CU0 reutiliza ese mecanismo con un archivo independiente para Clock. Ver [infraestructura](infraestructura-y-migracion.md) y [operación Oracle](operacion-oracle.md).

## Configuración y acceso

1. Una persona operadora autorizada habilita la API y crea el usuario API en Clock con alcance de lectura necesario. Verificar permisos disponibles por entorno y separar demo, prueba y piloto. El token de Servicios externos queda fuera de la configuración de CU0.
2. Crear un archivo JSON privado con campos `username` y `password`, ambos de tipo string. Usar un directorio del runtime privado fuera del checkout y del contenido servido. Basic requiere la contraseña recuperable, así que el control principal es el acceso al archivo. Restringir permisos del archivo y directorio al operador y a la identidad efectiva de la API según la configuración de despliegue. Usar acceso mínimo de lectura para el proceso y un montaje de solo lectura.
3. Propuesta de configuración. `CLOCK_API_CREDENTIALS_FILE` contiene solo la ruta interna, por ejemplo `/run/secrets/softwareclock.json`. El mecanismo de despliegue resuelve la ruta privada del host y monta el archivo únicamente en el servicio API. Excluir frontend, proxy, migraciones, contenedores auxiliares, imágenes, CI y archivos versionados. Mantener HTTPS hacia el origen comprobado.
4. Validar en composición que el archivo sea legible, de tamaño acotado y un objeto JSON con ambos campos definidos, no vacíos ni de solo espacios. Rechazar controles y dos puntos en el usuario Basic. Conservar los valores válidos sin recortarlos. El error de validación expone solo una categoría segura. Verificar permisos tanto en host como con el usuario efectivo del contenedor.
5. Transferir secrets por el canal privado de operación ya acordado. Cualquier respaldo necesario sigue el procedimiento cifrado y de acceso restringido vigente. No volcar valores en terminal, argumentos, historial, chat, tickets, variables VITE_*, logs ni comprobaciones de salud.

## Rotación

1. Coordinar ventana con Maxi. Confirmar con el proveedor si se puede solapar la credencial anterior y la nueva, y qué sucede con los tokens ya emitidos. Preparar recuperación según ese comportamiento.
2. Generar o sustituir la pareja desde el portal autorizado y preparar un archivo nuevo con los mismos controles de acceso. Validar su forma sin mostrar valores. Reemplazarlo de forma atómica y recrear el servicio API para aplicar el montaje actualizado y cargar el secret. Confirmar que el runtime ve el archivo nuevo. Un reinicio de backend también invalida las sesiones KUME por su diseño en memoria. Avisar a administración y verificar el nuevo login.
3. Ejecutar una autenticación y una lectura autorizada desde backend. Registrar fecha, entorno, responsable y resultado sanitizado. Si la credencial anterior sigue activa y la nueva ya funciona, deshabilitar la anterior conforme al procedimiento del proveedor. Confirmar el efecto sobre tokens previos sin recopilar sus valores.
4. Si falla la rotación, recuperar el archivo previo únicamente si la credencial sigue vigente y es segura. Si fue revocada o comprometida, emitir una nueva. Limpiar copias temporales y verificar disponibilidad de KUME. El token se recupera por Basic a demanda y permanece en memoria.

[Caso de uso](../functional/softwareclock/autenticacion.md) · [Diseño técnico](../specs/011-softwareclock-auth/technical-spec.md)
