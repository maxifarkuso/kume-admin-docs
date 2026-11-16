# Recuperación controlada de roles de Personal

Preparado el 16 de noviembre de 2026 por autorización de Maxi. Operación existente
`expense-staff-20261116-131318`, backend `774f5b862c7c80fa6ca90b54a38890a31a9e73b5`.
El operador reportó vencimiento aplicado, roles sin finalizar, ficha de prueba
eliminada, tabla vacía y constraint antiguo validado. Revalidar en destino: ese
reporte no sustituye el inspector ni la ventana. No ejecutar si ya cambió el estado.

Esta guía conserva config, respaldo y journal existentes. No ejecutar preparar,
respaldo, inicializar ni cambiar el ID. No instalar dependencias en el host ni
modificar la distribución activa: usar una copia completa fijada del motor nuevo.

## Preparar motor en paralelo

El SHA completo del motor se entrega al publicar el cambio. Sustituir el marcador
antes de ejecutar; una rama mutable no es una revisión aprobada.

```bash
export KUME_MOTOR_REV="REEMPLAZAR_POR_SHA_COMPLETO_DEL_MOTOR_PUBLICADO"
export KUME_MOTOR="$HOME/.local/share/kume-admin/motor-$KUME_MOTOR_REV"
export KUME_OP="expense-staff-20261116-131318"
export KUME_DIR="$HOME/.local/share/kume-admin/preparacion-$KUME_OP"
umask 077

git clone --no-checkout https://github.com/maxifarkuso/kume-admin-docs.git "$KUME_MOTOR"
git -C "$KUME_MOTOR" checkout --detach "$KUME_MOTOR_REV"
git -C "$KUME_MOTOR" rev-parse HEAD
git -C "$KUME_MOTOR" status --short
(
  cd "$KUME_MOTOR"
  sha256sum --check docs/devops/sql/staff-roles-recovery.sha256
)
bash -n "$KUME_MOTOR/scripts/oracle-admin.sh"
bash "$KUME_MOTOR/scripts/oracle-admin.sh" migraciones --help
```

Exigir SHA coincidente, checkout limpio y checksums correctos. Si falla acceso,
detenerse; no crear credenciales ni aceptar hosts desconocidos. Revisar el código
y los dos SELECT antes de aprobarlos. La copia nueva no modifica PATH ni instalación previa.

## Copiar y aprobar los SELECT privados

El inspector exige: vencimiento aplicado e índice válido, checksum correcto,
constraint anterior de roles completo/validado y tabla vacía, un solo intento de
roles sin finished y sin otra migración fallida activa. Admite ese mismo intento
antes/después de marcarlo revertido; el motor compara el ID/historial exactos.
No usarlo para otra migración ni después de agregar fichas sin revisar el caso.
El final verifica vencimiento y roles nuevos, una aplicación exitosa de cada uno
y ninguna migración fallida sin revertir. Los checksums se contrastan además
contra todos los archivos por el motor. No modifica los verificadores originales.

```bash
python3 - <<'PY'
import os
from pathlib import Path

source = Path(os.environ["KUME_MOTOR"]) / "docs/devops/sql"
destination = Path(os.environ["KUME_DIR"])
for name in ("staff-roles-recovery-inspection.sql", "staff-roles-recovery-final.sql"):
    target = destination / name
    with target.open("xb") as output:
        output.write((source / name).read_bytes())
    target.chmod(0o600)
    print(target)
PY

export KUME_INSPECTION_SHA="$(sha256sum "$KUME_DIR/staff-roles-recovery-inspection.sql" | cut -d ' ' -f 1)"
export KUME_FINAL_SHA="$(sha256sum "$KUME_DIR/staff-roles-recovery-final.sql" | cut -d ' ' -f 1)"
KUME_ADMIN=(bash "$KUME_MOTOR/scripts/oracle-admin.sh")
```

Si los archivos ya existen, no sobrescribirlos: comparar con las plantillas antes
de reutilizarlos. Los hashes anteriores aprueban exactamente los archivos revisados.

## Recuperar, habilitar, aplicar y verificar

Mantener ventana sin escrituras ni despliegues. Revisar cada salida antes de la
siguiente etapa aunque se entregue la lista completa. `recuperar-fallida` escribe
metadatos de Prisma; `aplicar` ejecuta únicamente SQL pendiente. Las frases se
pegan en el prompt de la herramienta, no como comandos Bash.

```bash
"${KUME_ADMIN[@]}" migraciones recuperar-fallida \
  --config "$KUME_DIR/destino.json" --operacion "$KUME_OP" \
  --migracion 202611160002_staff_roles \
  --inspeccion-sql "$KUME_DIR/staff-roles-recovery-inspection.sql" \
  --inspeccion-sha256 "$KUME_INSPECTION_SHA" \
  --verificacion-sql "$KUME_DIR/staff-roles-recovery-final.sql" \
  --verificacion-sha256 "$KUME_FINAL_SHA"

"${KUME_ADMIN[@]}" migraciones habilitar-reintento \
  --config "$KUME_DIR/destino.json" --operacion "$KUME_OP" \
  --inspeccion-sql "$KUME_DIR/staff-roles-recovery-inspection.sql" \
  --inspeccion-sha256 "$KUME_INSPECTION_SHA"

"${KUME_ADMIN[@]}" migraciones aplicar \
  --config "$KUME_DIR/destino.json" --operacion "$KUME_OP"

"${KUME_ADMIN[@]}" migraciones verificar \
  --config "$KUME_DIR/destino.json" --operacion "$KUME_OP"

"${KUME_ADMIN[@]}" migraciones estado \
  --config "$KUME_DIR/destino.json" --operacion "$KUME_OP"

"${KUME_ADMIN[@]}" migraciones retirar \
  --config "$KUME_DIR/destino.json" --operacion "$KUME_OP"
```

Avanzar solo tras `Etapa completada` de cada acción y ninguna pendiente al final.
Si una escritura falla, detener la secuencia y conservar evidencia: no repetir
resolve/aplicar, no editar journals y no cambiar ID. Un resolve incierto queda
fuera de la recuperación automática. Retirar herramientas solo tras verificar o
como parte de un plan de diagnóstico específico; no sustituye resolver incertidumbre.
No hay despliegue implícito del producto. Conservar copia y distribución anterior:
volver a la herramienta antigua no revierte SQL y esa versión no comprende este
historial revertido; usar la nueva distribución para futuras operaciones.
