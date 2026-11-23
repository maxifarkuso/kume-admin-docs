# CU0 — Especificación funcional

**Estado al 23 de noviembre de 2026.** Alcance y requisitos de seguridad instruidos por Maxi. Política de arranque pendiente de confirmación en GrillMe. El diseño técnico es una propuesta. CU0 aún no está implementado. Maxi verificó manualmente la autenticación y una lectura de asistencias. Esa evidencia no cubre renovación, revocación ni errores.

## Criterios de aceptación

| ID | Resultado observable |
| --- | --- |
| CA1 | Con secrets válidos y memoria vacía, la primera lectura obtiene un token mediante Basic y consulta con Bearer. Un HTTP 200 con código de error, JSON inválido o token inválido impide la consulta. |
| CA2 | CU1, CU2 y CU3 comparten una sola instancia del mecanismo por proceso. Una ráfaga sin token espera una sola autenticación. Si falla, los participantes reciben el mismo resultado seguro. Con token disponible se reutiliza. Un reinicio empieza con memoria vacía. |
| CA3 | Una señal confirmada de token rechazado invalida esa generación y coordina una sola renovación concurrente. Cada lectura admite una repetición como máximo. Un rechazo tardío no invalida un token más nuevo. Un 403 genérico no renueva. |
| CA4 | Configuración inválida, credenciales rechazadas, timeout, límites y caída se distinguen internamente sin revelar valores. Se respeta la política de arranque aprobada y se acotan intentos y tiempos. |
| CA5 | Un fallo externo no invalida la cookie ni la sesión de KUME, no se traduce en un desafío de login y no borra, cambia ni presenta como vacío el último resultado local válido. |
| CA6 | Usuario y contraseña provienen de un archivo de secrets de solo lectura accesible por el backend. Token exclusivamente en memoria. Ausencia de valores en API, repositorio, archivos versionados, navegador, variables VITE_*, persistencia, logs, trazas, métricas y textos de error. Incluye errores con credenciales reflejadas por el proveedor. |
| CA7 | Pruebas reproducibles con proveedor simulado, fixtures ficticios y tiempo controlado. Evidencia real registrada por separado, como estados y códigos permitidos, sin cuerpos, cabeceras sensibles ni datos personales. |

CU0 cubre autenticación y acceso compartido de solo lectura. Las rutas, la persistencia y las reglas de negocio de cada consumidor pertenecen a sus propias especificaciones. Ver [caso de uso](../../functional/softwareclock/autenticacion.md), [plan](plan.md) y [tareas](tasks.md).
