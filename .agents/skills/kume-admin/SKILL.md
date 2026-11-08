---
name: kume-admin
description: Instalar, actualizar o comprobar kume-admin; conservar consultas de infraestructura y gestionar migraciones explícitas con respaldo, confirmación y evidencias.
---

# KUME — Administración de infraestructura y migraciones

Usar cuando se pida instalar, revalidar o adaptar kume-admin, consultar memoria,
disco, Docker, releases o estados operativos. Incluye migraciones Prisma explícitas
según autorización de la sesión. No es una habilidad de despliegue, limpieza Docker, autenticación o traslado completo de datos.

## Cargar contexto

1. Leer [AGENTS.md](../../../AGENTS.md) del repositorio.
2. Leer [administracion-oracle.md](../../../docs/devops/administracion-oracle.md): fuente
   propietaria de comandos, instalación por pasos, checksum histórico y PATH.
3. Leer [operacion-oracle.md](../../../docs/devops/operacion-oracle.md): evidencia reportada
   y pendientes. No asumir que ese registro describe el estado actual del destino.
4. Inspeccionar [oracle-admin.sh](../../../scripts/oracle-admin.sh) de la revisión
   elegida. No ejecutar un script descargado de una rama mutable sin revisión.

Para migraciones leer además [migraciones-admin.md](../../../docs/devops/migraciones-admin.md)
y [spec 002](../../../docs/specs/002-admin-migrations/spec.md), incluido diseño,
plan y evidencia. El permiso para desarrollar localmente no autoriza Oracle.

## Procedimiento

- Identificar máquina destino, sistema operativo, usuario y sesión de terminal.
  Si es la computadora de trabajo administrada, no eludir políticas para probar
  túneles; usar solo los accesos autorizados y dejar pruebas externas pendientes.
- Si se opera en una terminal del usuario, explicar **un comando por vez** y
  esperar su resultado. No enviar un instalador que agrupe todo sin observación.
- Comprobar dependencias y destinos antes de escribir. Ejecutar como usuario de
  despliegue, sin sudo global; las consultas Docker gestionan sudo por separado.
  No instalar paquetes ni conceder privilegios por inferencia.
- Si la utilidad ya existe, obtener su checksum y revisar la versión antes de
  actualizar; preservar el archivo y no reemplazar contenido distinto en silencio.
- Elegir commit aprobado y checksum correspondiente. El procedimiento documenta
  la versión instalada en Oracle; una versión distinta requiere su propio hash.
- Descargar a un archivo temporal separado, comprobar checksum completo y sintaxis
  Bash; detenerse si hay discrepancias, sin ejecutar el contenido.
- Instalar con permisos de usuario en ~/.local/bin/kume-admin según la guía.
  No tocar aplicaciones, secrets, estados o perfiles ajenos.
- Probar ayuda mediante ruta absoluta y luego estados, salud y Docker por separado.
  No crear estados de despliegue para hacer pasar una comprobación en destino vacío.
- Comprobar command -v kume-admin. Si falta en la sesión actual, añadir
  ~/.local/bin al PATH temporal según la guía, conservando las otras entradas.
- Inspeccionar perfiles antes de editar: Ubuntu puede tener ya el bloque
  condicional en ~/.profile. Si existe, probar otra sesión sin duplicarlo.
  Si no existe o falla, identificar el perfil real del shell antes de adaptarlo.
- Mantener la sesión de acceso funcional abierta mientras se verifica el comando
  desde una segunda sesión. No reiniciar la máquina para probar el PATH.

## Adaptación a una máquina local

Comparar sistema, rutas, servicios, puertos y acceso a Docker con el script.
No asumir que Windows nativo, WSL o un Linux distinto se comportan como Oracle.
Si se requiere adaptar código, hacerlo en la fuente versionada, comprobarlo y
calcular una huella nueva; no modificar una descarga y atribuirle el hash anterior.
Instalar la utilidad no instala ni migra el producto: la migración completa se
rige por [infraestructura-y-migracion.md](../../../docs/devops/infraestructura-y-migracion.md).

## Límites y cierre

No pedir claves privadas, contraseñas, runtime.env, variables de contenedores o
logs privados. No borrar imágenes/volúmenes, reiniciar, publicar, recuperar
transacciones ni abrir puertos por inferencia. Las consultas existentes mantienen su garantía de lectura.
Migraciones solo mediante etapas explícitas del motor, destino/revisión aprobados,
locks y ventana coordinada, respaldo comprobado y confirmación literal antes de SQL.
No convertir una inicialización excepcional en flujo automático. Ante running o
uncertain inspeccionar y verificar, sin repetir SQL. Retirar solo el contenedor
propio; conservar evidencias y distinguir índice legible de restauración real.
El JSON de estado y sus rutas no acreditan CI, integridad, identidad Docker,
restauración o acceso de navegador. Tratar cada evidencia por separado.
Registrar revisión, checksum, ruta, PATH y consultas efectivamente probadas;
distinguir documentado, instalado y comprobado. Indicar lo pendiente sin inferirlo.
Esta SKILL es un recurso versionado del repositorio, no un plugin global instalado
ni un servicio en Oracle; no afirmar que fue activada en otra herramienta.
