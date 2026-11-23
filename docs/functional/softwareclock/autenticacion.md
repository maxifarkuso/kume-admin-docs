# CU0 — Autenticación con SoftwareClock

**Alcance solicitado por Maxi.** CU0 habilita las lecturas de Clock iniciadas por CU1, CU2 y CU3 mediante un único mecanismo de backend. El navegador consume la API de KUME con su sesión de administración habitual.

- **Disparador.** Un caso consumidor autorizado necesita consultar SoftwareClock.
- **Precondiciones.** El módulo API está habilitado en Clock y la pareja del usuario API está configurada en un secret privado del backend.
- **Flujo principal.** El backend obtiene un token si hace falta, valida la respuesta y usa el token en la consulta externa. Las solicitudes siguientes comparten el token del proceso. El consumidor recibe datos validados de su operación.
- **Alternativas.** Si Clock rechaza el token con una señal confirmada, el backend coordina su renovación y permite una sola repetición de la lectura. Si la configuración es inválida o Clock falla, el consumidor recibe un fallo de integración seguro.
- **Postcondiciones.** El resultado externo válido queda disponible para el consumidor. Ante un fallo, se conservan los datos locales y la sesión de KUME. Los datos locales disponibles pueden seguir consultándose según el contrato del caso consumidor.

[Especificación y criterios de aceptación](../../specs/011-softwareclock-auth/spec.md) · [Diseño técnico y secuencias](../../specs/011-softwareclock-auth/technical-spec.md) · [Configuración y rotación](../../devops/softwareclock-secrets.md)
