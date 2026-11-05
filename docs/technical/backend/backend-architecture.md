# KUME — Arquitectura backend

Estado: aprobado por Maxi; arquitectura limpia, tipado estricto y TypeBox confirmados. Fecha: 2 de noviembre de 2026.

## Unidad de despliegue y módulos

Una aplicación Fastify desplegable con PostgreSQL y archivos externos persistentes. “Monolito modular” describe esa unidad de despliegue; las capas e interfaces son obligatorias dentro de ella.

```text
src/
  composition/                     # arranque, configuración e inyección
  modules/
    expenses/
      domain/                      # entidades, valores e invariantes
      application/
        ports/                     # interfaces requeridas por casos de uso
        use-cases/                 # entradas y resultados propios
      infrastructure/
        persistence/               # Prisma, mappers, consultas
      http/                        # rutas, handlers y TypeBox
    staff/
    assignments/
    categories/
    courses/
    workshops/
  infrastructure/                  # clientes compartidos y adaptadores técnicos
    persistence/
    files/
  http/                            # manejo común de errores y plugins HTTP
prisma/
  migrations/
```

Crear unidades según necesidades reales. Dominio puede implementarse con clases o funciones y tipos que encapsulen invariantes; no imponer herencia ni clases anémicas. No agregar directorios genéricos utils/common para responsabilidades que tienen dueño.

## Regla de dependencias

| Consumidor | Dependencias permitidas |
|---|---|
| domain | TypeScript y conceptos propios de dominio |
| application | domain y puertos definidos hacia el interior |
| infrastructure | puertos/application y domain que adapta, librerías externas |
| http | entradas/resultados de application, esquemas HTTP y Fastify |
| composition | capas necesarias para construir y conectar implementaciones |

domain no importa application ni detalles externos. application no importa Fastify, Prisma, TypeBox, filesystem, variables de entorno ni adaptadores. Los handlers HTTP no importan persistencia; reciben casos de uso. composition no contiene reglas de negocio.

Un módulo colabora con otro mediante un contrato de aplicación explícito; no consulta sus tablas ni importa adaptadores internos. Evitar ciclos. Una operación transversal debe tener un dueño y una frontera transaccional definidos, sin una cadena circular de servicios.

## Puertos, tipos y objetos

Interfaces de repositorio específicas expresan necesidades de casos de uso. Un puerto pertenece a quien lo necesita, normalmente application/ports; una abstracción puramente de dominio se coloca en domain solo cuando el dominio la requiere. No imponer IRepository<T> ni una interfaz por clase.

Inyectar dependencias por parámetros/constructores y conectarlas explícitamente en composition. No contenedor de DI obligatorio ni service locator. Reloj, generación de identificadores y servicios externos se abstraen donde su variabilidad afecte reglas o pruebas.

TypeScript strict en todo el proyecto. unknown en límites externos hasta validar; uniones discriminadas para resultados esperados, chequeos exhaustivos y tipos con significado de dominio. No usar any, doble aserción o non-null assertions para silenciar defectos. Toda excepción requiere justificación localizada.

DTO HTTP, modelos de aplicación/dominio y registros Prisma son representaciones separadas. Mapear en los adaptadores; no exponer Prisma.Decimal, enums generados, TransactionClient ni tipos de petición Fastify al núcleo. Compartir estructuras simples solo cuando el concepto y su dueño sean realmente los mismos.

Importes del dominio usan una representación decimal exacta independiente de Prisma; elegir implementación al inicializar, sin float contable ni librería nueva implícita. Fechas civiles y timestamps son conceptos distintos. No convertir DATE a instante por comodidad. Definir “hoy” del negocio y probar bordes temporales antes de implementar validaciones.

## Flujo de una operación

1. HTTP valida estructura, parámetros y cuerpo con TypeBox/JSON Schema; adapta identidad autorizada cuando se resuelva autenticación.
2. El caso de uso recibe entrada propia y colaboradores por puertos, obtiene entidades y coordina la operación.
3. El dominio comprueba invariantes y produce cambios válidos.
4. Persistencia mapea y guarda de manera atómica según el caso de uso.
5. HTTP transforma resultado o error esperado al contrato público.

Esquemas HTTP validan sintaxis y forma; no sustituyen invariantes. Los errores esperados se modelan como resultados discriminados; HTTP decide sus estados y problem+json. Errores inesperados conservan causa para diagnóstico interno, con respuesta pública segura y logs sin datos sensibles.

## Persistencia, transacciones y concurrencia

Prisma implementa acceso a PostgreSQL. SQL adicional y errores del proveedor permanecen en persistencia. Migraciones versionadas deben conservar checks, índices únicos parciales, unicidad normalizada, triggers y ON DELETE RESTRICT de docs/technical/backend/database-design.md. No sustituir restricciones por consultas previas, ni usar db push como procedimiento de producción.

El caso de uso define qué debe ser atómico; un puerto de transacciones/unidad de trabajo permite ejecutarlo sin nombrar Prisma. Los repositorios usados dentro de una operación deben compartir la transacción real. No abrir transacciones independientes por cada repositorio ni mantenerlas abiertas durante transferencias de archivos o llamadas de red.

Control optimista aprobado: leer versión y comparar/incrementar atómicamente al escribir. Una lectura previa seguida de update sin condición no evita pérdida de cambios. Los fallos por versión no se reintentan con la versión nueva automáticamente. Incorporar al contrato y migraciones el alcance de recursos, token, respuesta y código de conflicto antes de implementar. No asumir un version actual en tablas ni cabecera existente.

El versionado no protege por sí solo reglas entre filas. Asignar, inactivar y modificar turnos requiere coordinación transaccional de los recursos afectados, con restricciones PostgreSQL como última defensa. Concretar bloqueo/aislamiento y orden consistente al implementar esas operaciones; no declarar probado ese comportamiento mediante mocks.

## Archivos y seguridad

Puerto de almacenamiento con claves relativas opacas; adaptador filesystem externo. Un único archivo por carga, entre 1 y 10.485.760 bytes, PDF/JPEG/PNG, validando extensión, MIME y firma. Limitar streaming y limpiar temporales; el nombre original nunca decide una ruta. No enviar buffers de archivo al dominio ni convertir el filesystem en transacción SQL.

Conservar la secuencia de docs/technical/api-design.md: validar temporal, almacenar archivo nuevo, confirmar datos, compensar el nuevo si falla la base y borrar el anterior solo tras commit. Limpieza fallida se registra para recuperación; no ocultarla ni borrar archivos aún referenciados. Respaldar base y archivos consistentemente.

No elegir mecanismos de sesión en esta guía. Definirlos en una decisión separada antes de implementar autenticación y autorizar datos reales. Autorización debe proteger cada operación y descarga del lado servidor. Las fichas de personal no son cuentas de acceso. Validar configuración al arrancar, centralizar logs seguros, limitar CORS al origen configurado y respetar secretos fuera del código.

## Pruebas y controles

Vitest para entidades, valores, invariantes y casos de uso con dobles tipados de puertos. Cubrir errores, restricciones de estado, conflictos y fallos de compensación sin servidor/base. Tests deterministas con reloj y IDs controlados donde corresponda; no usar espera real para probar vencimientos.

Configurar lint de imports al inicializar para impedir domain → capas externas, application → adaptadores y http → persistencia, además de ciclos entre módulos. La revisión manual complementa el control. Las pruebas de integración siguen pendientes de acuerdo; las unitarias no verifican restricciones reales, aislamiento ni migraciones.

Referencias: [TypeScript strict](https://www.typescriptlang.org/tsconfig/strict.html), [Fastify validation](https://fastify.dev/docs/latest/Reference/Validation-and-Serialization/), [Fastify Type Providers](https://fastify.dev/docs/latest/Reference/Type-Providers/), [Prisma transactions](https://www.prisma.io/docs/orm/prisma-client/queries/transactions), [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html). Revisar compatibilidad de TypeBox, su type provider, Fastify y OpenAPI antes de fijar versiones.
