# Oracle — Registro de instalación y funcionamiento

Registro consolidado: 4 de noviembre de 2026 (America/Montevideo).
Fuentes: resultados de comandos aportados por Maxi, ejecución GitHub Actions y
confirmación de visualización desde Windows personal. No es una inspección en
vivo de la VM desde Codex; revalidar antes de nuevas operaciones.

## Infraestructura preparada e instalación ejecutada

- VM Ubuntu 24.04.5 LTS, x86_64, aproximadamente 952 MiB RAM, sin swap.
- Antes de agregar Nginx se midieron 590 MiB de RAM disponible y 40 GB de disco
  libre sobre raíz de 45 GB. No son mediciones actuales tras la instalación.
- Nginx y nginx-common 1.24.0-2ubuntu7.19 instalados. Unidad predeterminada nginx
  enmascarada antes de apt; listeners comprobados sin nuevos puertos públicos.
- Unidad exclusiva kume-frontend.service: active, running y enabled, según salida
  aportada por Maxi. Sintaxis Nginx y unidad systemd verificadas en la VM.
- Nginx sirve /srv/kume-frontend/current y escucha solo en 127.0.0.1:8080.
- Backend real en 127.0.0.1:3001; PostgreSQL sin publicación de puerto en el host.
  No se agregaron reglas públicas para frontend, API o base durante esta instalación.

## Entrega del frontend comprobada

Código: [merge del PR #3](https://github.com/maxifarkuso/kume-admin-fe/pull/3),
commit 259f133761d8775998fe79322d70af0eab51a134.

[Workflow manual 41715115105](https://github.com/maxifarkuso/kume-admin-fe/actions/runs/41715115105):
build, controles, artefacto, SSH y preparación terminaron correctamente. Primera
salida prepared, sin equipararla a servicio activo.
Maxi arrancó la unidad exclusiva y comprobó 127.0.0.1:8080. finalize-initial terminó
con result active y este estado:

```json
{
  "format": 1,
  "current": "259f133761d8775998fe79322d70af0eab51a134-41715115105-1",
  "pending": null,
  "previous": null
}
```

La finalización ejecutó probes de HTML/SPA/assets, bloqueos de salud, API ausente
y SQL interno según el instalador de esa revisión. Es una landing sin login,
CRUD, clientes HTTP ni datos reales. API 404 es respuesta esperada del backend
actual, no funcionamiento del contrato completo.
No hay entrega previa: reversión real no ensayada todavía.

## Backend y PostgreSQL conservados

Backend instalado declarado: f023a7bd7132b65a59497f4a6fda4452ee648058;
proyecto kume-backend, contenedor kume-backend-api-1.
GET /health devuelve HTTP 200 con status ok y database ok, probado en la VM
antes y después de preparar Nginx. No implementa autenticación ni CRUD.
No se modificaron APP_ORIGIN, cookies, CORS, secrets o migraciones.

PostgreSQL kume-infra-test-db-1 siguió activo y healthy; volumen
kume-infra-test_postgres_data presente. Red kume-infra-test_default compartida
con el backend real. Presencia y salud SQL no demuestran restauración ni reinicio.

Maxi detuvo únicamente kume-infra-test-api-1 con docker stop y conservó su
contenedor. Después figuró Exited (137); la causa exacta del SIGKILL no se
investigó y no acredita OOM. Puerto 3000 dejó de escuchar; backend y base siguieron
funcionando. No se ejecutó down -v, eliminación de volúmenes o limpieza de Docker.

La [memoria del smoke test](memoria-app-test-oracle.md) es histórica: no ejecutar
su retirada con Compose down en la instalación actual, porque PostgreSQL y red
son utilizados por el backend real.

## Acceso de prueba comprobado desde computadora personal

Maxi generó una clave personal en Windows y autorizó únicamente su parte pública
sin reemplazar las existentes. No se registran claves, frases o huellas aquí.
La clave de Actions permanece separada de la personal; por decisión explícita,
frontend/backend comparten la credencial de Actions y su rotación debe coordinarse.

PuTTY 0.85 en Windows personal: SSH como usuario de despliegue y túnel **Local**,
source 127.0.0.1:8080 hacia destination 127.0.0.1:8080. No permitir conexiones de
otros hosts al puerto local. Inicialmente solo había shell; se agregó la regla
con Change Settings, Add y Apply y se guardó la sesión para próximos accesos.

Maxi confirmó que Chrome mostró la landing en http://localhost:8080.
Esto acredita acceso externo restringido a la landing, sin abrir HTTP público.
El túnel requiere mantener PuTTY conectado y se cierra al terminar la sesión.
La computadora del trabajo administrada no se usa para intentar eludir restricciones.
Nuevas pruebas personales de navegador quedan pendientes hasta disponer de ese equipo.

## Utilidad kume-admin instalada y comprobada

Maxi instaló la utilidad el 4 de noviembre de 2026 como usuario de despliegue,
sin sudo global. Procedimiento propietario, comandos y adaptación a otra máquina:
[administración de Oracle](administracion-oracle.md#instalación-comprobada-y-repetible).

- Fuente de docs: commit 28d2460a0f75beac01bf7b02edec5b037e104054.
- Archivo descargado a ~/.local/bin/kume-admin.download; SHA-256 completo
  comparado y confirmado antes de instalar. La huella se conserva en la guía.
- Copia ejecutable: ~/.local/bin/kume-admin, instalada con modo 0700 en carpeta
  propia 0700, mediante install sin sudo.
- Ayuda, estados reales, salud y contenedores: salidas aportadas por Maxi.
  Frontend/backend con current definido, previous/pending null y rutas coherentes;
  backend/SQL correctos y frontend HTTP 200 text/html. Backend y PostgreSQL activos,
  API temporal detenida y conservada.
- Se confirmó después que todas las consultas del menú funcionaron en la VM.
- El comando corto inicialmente no existía en PATH. Un export temporal permitió
  usarlo; se comprobó que ~/.profile ya incluía ~/.local/bin condicionalmente.
  No se editaron perfiles. En una segunda sesión SSH command -v devolvió
  /home/ubuntu/.local/bin/kume-admin.

La disponibilidad en una sesión nueva no acredita persistencia de servicios tras
reiniciar Oracle. La utilidad no se actualiza automáticamente desde GitHub.
Habilidad para repetir el proceso: [kume-admin](../../.agents/skills/kume-admin/SKILL.md).
Instalación en otra máquina y migración completa del producto siguen sin probarse.

## Próximas verificaciones y exclusiones

- Ensayo real de actualización y reversión con dos releases válidas, sin tocar datos;
  Maxi acordó retomarlo al instalar authentication-foundation.
- Reinicio de VM coordinado y persistencia/arranque comprobados después.
- Medición actual de recursos tras Nginx y carga representativa antes del uso real.
- Autenticación integrada y desplegada por separado; origen/transporte/cookies coordinados.
- Dominio, HTTPS y renovación, revisión explícita de red antes de acceso público.
- Aislamiento de demo, respaldos y restauración real antes de datos reales.

Herramienta de consulta: [administración de Oracle](administracion-oracle.md).
Este registro no completa diseño de pantallas, no habilita piloto ni cambia el
contrato canónico o los requisitos de seguridad acordados.

## Mejora propuesta: revisión automática del backend

Estado: preparada para revisión por PR independiente; no integrada ni desplegada.
SDD documental: [001 — Revisión backend](../specs/001-backend-revision/spec.md).
Implementación y runbook propietarios en
[frontend 004](https://github.com/maxifarkuso/kume-admin-fe/blob/feat/automatic-backend-revision/docs/specs/004-backend-revision/spec.md) y
[operación frontend](https://github.com/maxifarkuso/kume-admin-fe/blob/feat/automatic-backend-revision/docs/deployment/oracle-test.md#revisión-automática-del-backend).

El workflow frontend conserva ejecución manual desde main. Para deploy, un job
con el environment oracle-test consulta por SSH el backend instalado antes del
build. Valida current/previous/pending, IDs completos, ausencia de pending y
GET http://127.0.0.1:3001/health con HTTP 200, status=ok y database=ok. Solo el SHA
completo pasa al empaquetado y al manifiesto existente; no se usa una variable
manual, una revisión de main ni una entrega anterior como fallback.

La consulta lee únicamente /home/ubuntu/kume-backend/state.json y el
deployment.lock existente en ese directorio. Usa un lock compartido no bloqueante,
compatible con otras consultas y excluyente con el lock exclusivo ya utilizado
por el gestor de despliegue backend. La publicación frontend retiene ese lock
mientras opera y revalida revisión y salud inmediatamente antes del journal y la
activación. Si cambió el SHA durante la preparación, aborta sin cambiar la versión
activa; las releases preparadas pueden conservarse. Las operaciones manuales que
ignoren ese lock no están coordinadas por este mecanismo.

La cuenta SSH existente debe poder atravesar esa ruta y leer ambos archivos.
No se amplían permisos ni se consulta runtime.env, configuración privada o
credenciales. restrict en authorized_keys no aísla los comandos de una cuenta
administrativa: conservar explícita esa limitación. Si falta acceso, falla; no
modificar ACL ni sudoers por inferencia. La consulta no crea ni escribe archivos
del backend y no instala servicios permanentes.

Ante SSH fallido, estado inválido, pending, backend no saludable, lock ocupado o
revisión incompatible, revisar la causa y el estado antes de repetir. No copiar
secrets, estado bruto ni respuestas remotas arbitrarias en logs. Se conservan
checksums, manifiestos, journal, recuperación, activación inicial guiada y rollback
contra el backend compatible; rollback no requiere construir otra release.

BACKEND_REVISION queda ignorada por el workflow nuevo. Retirar la variable solo
tras integrar la mejora y comprobar una ejecución manual con el SHA esperado.
No se retira en esta tarea. Para volver al workflow anterior, revertir el commit
de implementación del frontend y restaurar primero la variable con el SHA
realmente instalado. No requiere migración ni cambio de configuración de la VM.

Pendiente: integración y primera ejecución autorizada en Oracle. Las pruebas
locales no acreditan permisos SSH efectivos ni despliegue en la VM. La mejora
no depende de authentication-foundation ni cambia su rama o despliegue.
