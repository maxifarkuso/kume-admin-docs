# KUME — Arquitectura frontend

Estado: aprobado por Maxi; reglas confirmadas para la implementación. Fecha: 2 de noviembre de 2026.

## Estructura y dependencias

React + TypeScript + Vite, organizado por funcionalidad. Crear carpetas al existir código que las necesite, sin scaffolding vacío obligatorio.

```text
src/
  app/                     # router, providers y composición
  features/
    expenses/
      api/                 # funciones HTTP, query keys y hooks remotos
      components/          # presentación de esta funcionalidad
      forms/               # esquemas Zod y conversión de formularios
      pages/               # orquestación de pantallas
      model/               # transformaciones y estado propios
      index.ts             # API pública mínima
    staff/
    categories/
    courses/
    workshops/
  shared/
    api/                   # transporte y tipos generados
    ui/                    # componentes accesibles reutilizables
    dates/                 # manejo de fechas civiles e instantes
    money/                 # presentación decimal UYU
```

app puede importar APIs públicas de features y shared. Una feature puede importar shared; para colaborar con otra feature usar su API pública mínima y mantener un grafo acíclico. Si hay dependencia mutua, componer en app o extraer un concepto estable. shared nunca depende de features ni app. No exportar cada archivo ni usar barrels que creen ciclos. Los tests pueden permanecer junto al comportamiento probado.

## React y estado

- Componentes funcionales; hooks solo en el nivel superior de componentes o hooks propios. Nombres useX para hooks y PascalCase para componentes.
- Render puro, actualizaciones inmutables y claves estables. No mutar props ni guardar valores derivados redundantes en estado.
- Eventos procesan acciones de usuario; efectos sincronizan sistemas externos. No encadenar efectos para derivar estado o cargar datos que administra TanStack Query.
- React Router administra navegación; filtros compartibles y paginación se reflejan en la URL conforme diseño aprobado. Restaurar contexto al volver de formularios.
- TanStack Query administra datos remotos, estados de carga y caché. Query keys incluyen filtros y paginación; invalidar consultas afectadas al confirmar mutaciones. No reintentar escrituras ciegamente.
- Estado local para UI y React Hook Form para formularios. Context solo para dependencias o estado compartido estable que lo requiera. No agregar Redux/Zustand por anticipación.
- Optimizar con memoización solo ante necesidad comprobada; no ocultar efectos o dependencias incorrectos.

## HTTP, tipos y formularios

El transporte de shared/api centraliza base URL, serialización, normalización de problem+json y cancelación. Las funciones de cada feature expresan operaciones del contrato. No usar fetch directamente en componentes de presentación.

Generar tipos desde la revisión fijada de OpenAPI. No definir duplicados manuales de DTO ni editar código generado. El generador concreto y su versión se verificarán al inicializar y quedarán fijados como herramienta de desarrollo. Tipos estáticos no validan respuestas en ejecución: validar datos desconocidos en el límite cuando corresponda y no usar casts para asumir su forma.

Zod valida formularios con React Hook Form. Mantener separados valores de formulario, DTO y modelos de presentación; convertir explícitamente strings vacíos, opcionales y null. El backend mantiene la autoridad sobre reglas de negocio. Mostrar errores por campo y generales; no perder datos ingresados tras un fallo.

Importes viajan como strings decimales; nunca usar aritmética binaria de punto flotante para importes contables. Fechas civiles siguen YYYY-MM-DD; instantes se interpretan como UTC y se presentan según política del producto. La definición de “hoy” del negocio debe documentarse antes de implementar validaciones temporales; no inferirla del host.

## UX, accesibilidad y concurrencia

Todos los textos visibles en español, incluidos errores y estados vacíos. Traducir enums técnicos en mapas de presentación. HTML semántico, etiquetas asociadas, mensajes vinculados a campos, foco visible, teclado y foco/restauración correctos en diálogos. Usar botones y enlaces según su función.

No depender solo de color. Incluir carga, vacío, error, éxito, indisponibilidad y conflicto. Gasto anulado y ficha inactiva se presentan según sus restricciones. El frontend ayuda a prevenir operaciones inválidas; el backend siempre las vuelve a comprobar.

Ante edición obsoleta, conservar valores locales, avisar y ofrecer recargar; nunca sobrescribir ni reintentar automáticamente con una versión nueva. La forma exacta de versionado y respuesta necesita ampliación coordinada del contrato antes de implementar.

No introducir una librería visual o framework CSS como decisión implícita. Elegirlo al trabajar la UI con los diseños aprobados. El diseño de pantallas sigue en curso y no se sustituye por implementación React sin su aprobación.

## Seguridad y pruebas

No incluir secretos en VITE_*: esas variables son públicas. Evitar HTML no confiable y dangerouslySetInnerHTML. No guardar credenciales ni elegir transporte de sesiones; Q6 está pendiente. No cachear datos privados entre cuentas: al diseñar sesiones definir limpieza de caché al cerrar o cambiar de cuenta.

Vitest + React Testing Library para comportamiento aislado: formularios, traducción de errores, estados de consulta, filtros y conflictos. Usar interacciones y consultas accesibles, evitar asserts sobre internals y snapshots masivos. Sin Playwright en esta etapa. Las pruebas unitarias no acreditan integración real con backend o navegador completo.

Referencias: [React](https://react.dev/learn), [reglas de React](https://react.dev/reference/rules), [React Router](https://reactrouter.com/), [TanStack Query](https://tanstack.com/query/latest/docs/framework/react/overview), [React Hook Form](https://react-hook-form.com/), [Zod](https://zod.dev/), [WAI Forms](https://www.w3.org/WAI/tutorials/forms/). Verificar APIs contra las versiones instaladas.

## Sistema visual aprobado — 13 de noviembre de 2026

Aplicar las [reglas generales de interfaz](../../ui/sistema-visual.md) a los componentes compartidos y pantallas de todas las funcionalidades. El piloto de Gastos está aprobado visualmente, incluidas las correcciones de menú y altura uniforme de filtros. Esta decisión resuelve la dirección visual pendiente, pero no selecciona una librería visual ni autoriza nuevas dependencias de producción. La aprobación visual no acredita implementación ni modifica contratos o recorridos funcionales.
