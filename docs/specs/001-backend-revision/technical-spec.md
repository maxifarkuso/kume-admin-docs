# 001 — Diseño técnico documental

Estado: diseño para implementación.

La documentación propietaria de la implementación está en
[frontend 004](https://github.com/maxifarkuso/kume-admin-fe/blob/feat/automatic-backend-revision/docs/specs/004-backend-revision/technical-spec.md).

## Cambios previstos

Actualizar operacion-oracle.md con el flujo manual, la lectura de state.json y
deployment.lock y el health loopback. Enlazar la spec del frontend y la spec local
desde README.md sin copiar algoritmos ni documentación generada de otros repos.

Registrar que el lock compartido de consulta/publicación excluye el lock exclusivo
del backend, sin crear archivos, instalar servicios ni ampliar permisos. La cuenta
administrativa preexistente no se convierte en una cuenta aislada.

Explicar fallos por SSH, estado, pendiente, salud, lock y revisión incompatible;
revisar estado antes de repetir. La reversión del código requiere restaurar la
variable manual si se vuelve al workflow anterior. Su retirada es posterior al
merge y la verificación operativa explícita, fuera de esta sesión.

## Verificación

Comprobar enlaces relativos nuevos y Markdown, y ejecutar las pruebas operativas
existentes si están disponibles. Registrar por separado evidencia local y pendiente
en Oracle; sin cambios de contrato ni de revisión fijada de docs en consumidores.
