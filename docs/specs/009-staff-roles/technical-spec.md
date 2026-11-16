# Diseño técnico — Personal: nuevos roles

Eliminar assistant / Auxiliar. Incorporar cleaningAssistant / Auxiliar de limpieza, classroomAssistant / Auxiliar de sala, classroomLead / Encargada de sala y director / Directora. Conservar teacher y workshopInstructor. Maxi confirma que aún no existen fichas; no se requiere compatibilidad histórica ni reasignación de datos. Migración cambia CHECK, sin borrar ni modificar fichas y falla si aparecen roles retirados.

Mantener límites por funcionalidades y capas. OpenAPI canónico y tipos/esquemas generados en consumidores; UI en español. Coordinar frontend y backend cuando cambia el contrato.
