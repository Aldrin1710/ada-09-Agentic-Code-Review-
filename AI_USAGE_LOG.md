# AI Usage Log — ADA-09: Agentic Code Review

## Entry 01 - Definición y refinamiento del Change Request
- **Stage**: Human Gate 0 (Preparación y delimitación del alcance)
- **Prompt / Goal**: Analizar las opciones de cambio permitidas por la especificación de ADA-09 y definir un requerimiento acotado que afecte lógica y pruebas sin alterar la arquitectura base.
- **AI Contribution**: El asistente examinó el repositorio previo y el documento de requisitos, verificando que no existía funcionalidad previa de filtrado por dominio de correo, y propuso formalizar el requerimiento CR-03 con compatibilidad hacia atrás en `search_customers`.
- **Student Decision**: Aprobé la propuesta de filtrado por dominio de correo (`--domain` / argumento opcional `domain`), descartando cambios más invasivos en el modelo de datos. Autorizé formalmente el inicio de la implementación en `CHANGE_REQUEST.md`.
- **Impact**: Se delimitó con precisión el alcance antes de tocar una sola línea de código, garantizando que el agente desarrollador trabaje bajo criterios de aceptación objetivos y medibles.
