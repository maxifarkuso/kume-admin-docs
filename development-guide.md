# KUME — Guía de desarrollo

Estado: aprobado por Maxi; procedimientos para implementar al inicializar. Fecha: 2 de noviembre de 2026.

## Herramientas y versiones

npm en ambos repositorios, package-lock.json versionado y npm ci en CI. Elegir Node LTS con soporte vigente y compatibilidad verificada con Vite, Fastify y Prisma al inicializar. Fijar versión de runtime en configuración reproducible y engines; fijar imágenes y dependencias con lockfile. Evitar etiquetas latest. Node 22 y PostgreSQL 17 solo acreditan el ensayo anterior.

TypeScript strict. ESLint para reglas de lenguaje/framework e imports; Prettier como formateador de referencia para la inicialización. No discutir formato en revisiones. Revisar compatibilidad real de versiones y plugins antes de instalar; ninguna versión concreta queda inventada en este documento. Nuevas dependencias de producción fuera de las aprobadas requieren consulta y motivo.

Nombres técnicos en inglés: PascalCase para componentes/tipos, camelCase para valores/funciones y kebab-case para carpetas y archivos generales; componentes pueden usar PascalCase.tsx. Hooks useX. Tablas singulares y columnas snake_case mediante mapeo Prisma; JSON camelCase y rutas plurales kebab-case. Documentación y UI en español. No imponer convenciones que contradigan el contrato existente.

## Documentación disponible con un solo repositorio

La fuente editable es kume-admin-docs; los repositorios de código deben consumir una revisión inmutable, sin depender de tener los tres checkouts abiertos.

Al inicializar crear docs/reference.json con URL del repositorio docs, SHA completo de 40 caracteres, lista de rutas y SHA-256 de cada archivo sincronizado. Usar un único commit para reglas y contrato salvo una razón explícitamente documentada. Materializar esos archivos en docs/project conservando sus nombres. No guardar secretos ni configuración privada en ese snapshot.

Incluir AGENTS.md de docs como referencia, implementation-decisions.md, development-guide.md, stack-tecnologico.md, alcance-prototipo.md, api-design.md, openapi.yaml, database-design.md y la guía de arquitectura correspondiente. Incluir continuacion-diseno-pantallas.md para frontend e infraestructura-y-migracion.md cuando se trabaje operación.

Las copias son generadas y no se editan directamente. Un script de sincronización a crear obtiene una revisión explícita, verifica hashes y actualiza manifiesto/copia en un mismo cambio. El chequeo local/CI comprueba manifiesto, hashes y regeneración sin descargar main. Acceso remoto con credenciales fuera del repositorio; el CI ordinario debe funcionar con el snapshot versionado.

Bootstrap cuando todavía no existe docs/reference.json: obtener un commit aprobado de https://github.com/maxifarkuso/kume-admin-docs, leer sus guías y crear el mecanismo anterior como parte de la inicialización. No inventar un SHA para las guías nuevas: se fija después de incorporarlas y confirmar el commit. La revisión fcc2587 describe la base leída antes de estas reglas, no contiene estas reglas nuevas.

## Contrato OpenAPI

openapi.yaml de docs es canónico. TypeBox implementa esquemas HTTP del backend; no se convierte en una segunda fuente independiente ni sobrescribe el contrato aprobado.

Para cambiar API:

1. Proponer y aprobar cambios públicos en docs. Reconciliar api-design.md y database-design.md cuando corresponda, con ejemplos, estados y errores.
2. Validar OpenAPI y evaluar compatibilidad. Una ampliación interna compatible no es autorización para cambiar contratos públicos sin acuerdo.
3. Fijar el commit resultante en cada consumidor y regenerar tipos frontend de forma determinista. Elegir y fijar generador y versión al inicializar; prohibido editar el resultado.
4. Adaptar TypeBox, rutas y mappers backend. Comprobar correspondencia semántica de rutas, verbos, parámetros, cuerpos, respuestas y errores frente al contrato fijado. Documentar las normalizaciones entre OpenAPI y JSON Schema; no comparar solo texto ni nombres de tipos.
5. Coordinar despliegue compatible y enlazar cambios entre repositorios. No consumir en producción un campo que el backend desplegado todavía no soporta.

El contrato actual usa OpenAPI 3.1; verificar esa compatibilidad con las herramientas elegidas. El generador de tipos y el comparador/validador se eligen al inicializar. contract:check debe fallar por tipos generados desactualizados o divergencia de esquemas, no limitarse a comprobar que existe openapi.yaml. Verificar esquemas no demuestra que la implementación ejecutada cumpla el contrato: esa cobertura de integración está pendiente.

## Flujo Git y autonomía

- Docs: directamente sobre main según acuerdo existente. Antes de cambiar de rama comprobar cambios y referencias; sin reset forzado ni sobrescrituras.
- Frontend/backend: ramas cortas por cambio y pull request a main. Descripción con problema, comportamiento final y validación. CI obligatoria antes de integrar. Configuración de protección de rama y permisos reales se verifica al habilitar repositorios; este texto no los configura.
- No crear commits ni hacer push salvo petición explícita. Una instrucción posterior que los autorice es suficiente; no pedir confirmación repetida.
- Autonomía para detalles internos, correcciones y pruebas dentro de las convenciones. Consultar antes de cambiar stack, dependencias de producción no acordadas, contratos públicos, permisos o cambios destructivos en datos. Mostrar primero el cambio concreto y su impacto siempre que sea posible.
- No desplegar, borrar infraestructura o contratar servicios por inferencia. Respetar costo cero y autorizaciones concretas de la sesión.

## Comandos objetivo y CI

Crear estos scripts en package.json de cada repositorio de código y documentar requisitos en su README. Hasta la inicialización no se consideran disponibles.

| Comando | Finalidad |
|---|---|
| npm run format:check | Formato sin modificar archivos |
| npm run lint | Reglas de lenguaje, React donde aplique y límites de imports |
| npm run typecheck | TypeScript sin emitir |
| npm run test:unit | Suite Vitest sin watch; frontend con React Testing Library |
| npm run build | Compilación de producción |
| npm run contract:check | Snapshot/hashes, contrato y generación/correspondencia de esquemas |

CI de PR ejecuta npm ci y estos controles sobre versiones fijadas, sin secretos ni datos reales. No afirmar suite exitosa si no hay tests o se usó una opción que acepta ausencia de tests. No desactivar errores, saltar tests ni reducir garantías para obtener un check verde.

Al inicializar backend configurar Prisma generate según el build. Validación del schema y revisión de migraciones son controles estáticos útiles; no equivalen a aplicar SQL en PostgreSQL. No ejecutar automáticamente migraciones sobre datos reales desde una PR.

Para docs, comprobar Markdown y enlaces locales de los archivos tocados; si cambia OpenAPI, validar el contrato. No imponer npm ni crear package.json en docs solo para simular la CI de código.

## Política de pruebas de esta etapa

Unitarias en frontend y backend. Frontend: comportamiento de componentes, formularios, errores y estado con colaboradores controlados. Backend: invariantes y casos de uso con dobles de puertos. Tests deterministas y nombres que expresan escenarios y resultados; probar regresiones relevantes, sin cobertura porcentual arbitraria ni snapshots indiscriminados.

Playwright queda para una etapa posterior y no se instala ahora. Pruebas de integración no están acordadas todavía. No introducir Fastify.inject + PostgreSQL real como obligación aprobada ni afirmar verificaciones de SQL, sesiones, concurrencia real, navegador o almacenamiento real basándose en mocks. Las verificaciones operativas previas al piloto que ya exige alcance-prototipo.md se mantienen vigentes.

## Criterio de entrega de un cambio

- Implementa el alcance aprobado y no decide pendientes implícitamente.
- Respeta límites de módulos/capas, tipos, contrato fijado y reglas de seguridad.
- Tiene pruebas unitarias pertinentes y controles aplicables ejecutados; registrar lo que no pudo verificarse y por qué.
- Actualiza documentación y referencias cuando cambian decisiones.
- No incluye datos reales, secretos ni archivos temporales; fixtures sintéticos y .env.example sin valores privados.
- Explica riesgo o limitación material: pruebas unitarias no prueban sistema integrado.

Esto define entrega de código revisable, no autorización para piloto real. Para el piloto siguen siendo obligatorios HTTPS, autenticación/autorización, persistencia, aislamiento demo y restauración comprobada según los documentos operativos.
