# CU0 — Plan de implementación y verificación

1. **Cerrar diseño.** Confirmar comportamiento de arranque con Maxi. Validar el código de éxito de autenticación y señales del proveedor con evidencia sanitizada. Identificar límites del transporte, pausas y requisitos operativos antes de habilitar la integración.
2. **Construir la infraestructura.** Tras aprobación, fijar referencia documental inmutable según la guía de backend. Implementar carga privada, transporte y coordinación en el backend. Cablear una instancia compartida en composición. Verificar con operaciones de lectura ficticias antes de conectar los consumidores reales.
3. **Verificar seguridad y regresión.** Ejecutar los controles definidos por el backend y las pruebas de [tareas](tasks.md). Comprobar que un error de Clock no afecta sesión ni datos locales.
4. **Validar de forma controlada.** Con autorización operativa y un entorno autorizado, probar autenticación y una lectura de Clock minimizada. Registrar evidencia real por separado. Habilitar únicamente comportamientos respaldados por el contrato del proveedor.
5. **Entregar para revisión.** Documentación aquí, implementación futura en la rama de backend según su AGENTS. La publicación y el despliegue requieren sus autorizaciones vigentes. CU1–CU3 incorporan el adaptador en sus propias entregas.

[Especificación funcional](spec.md) · [Especificación técnica](technical-spec.md) · [Configuración y rotación](../../devops/softwareclock-secrets.md)
