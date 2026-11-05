# AI Usage Log — ADA-09: Agentic Code Review

## Entry 01 - Definición y refinamiento del Change Request
- **Stage**: Human Gate 0 (Preparación y delimitación del alcance)
- **Prompt / Goal**: Analizar las opciones de cambio permitidas por la especificación de ADA-09 y definir un requerimiento acotado que afecte lógica y pruebas sin alterar la arquitectura base.
- **AI Contribution**: El asistente examinó el repositorio previo y el documento de requisitos, verificando que no existía funcionalidad previa de filtrado por dominio de correo, y propuso formalizar el requerimiento CR-03 con compatibilidad hacia atrás en `search_customers`.
- **Student Decision**: Aprobé la propuesta de filtrado por dominio de correo (`--domain` / argumento opcional `domain`), descartando cambios más invasivos en el modelo de datos. Autorizé formalmente el inicio de la implementación en `CHANGE_REQUEST.md`.
- **Impact**: Se delimitó con precisión el alcance antes de tocar una sola línea de código, garantizando que el agente desarrollador trabaje bajo criterios de aceptación objetivos y medibles.

## Entry 02 - Plan del Coder Agent y validación del diseño
- **Stage**: Fase 1 (Coder Agent - Planificación)
- **Prompt / Goal**: Solicitar al agente desarrollador que formule un plan de implementación acotado antes de escribir código, respetando los límites de capas y los contratos existentes.
- **AI Contribution**: El Coder Agent elaboró un plan de cinco pasos divididos entre la capa de servicio (`src/service.py`), la interfaz de usuario (`src/cli.py`), las pruebas automatizadas y la matriz de trazabilidad en `docs/traceability.md`.
- **Student Decision**: Revisé el plan y verifiqué que no pretendiera modificar `data/customers.json` ni alterar las clases del modelo, asegurando que el parámetro `domain` mantuviera el valor predeterminado `None` para no romper llamadas existentes.
- **Impact**: Se evitó que el agente realizara refactorizaciones innecesarias o alterara capas protegidas por la arquitectura.

## Entry 03 - Implementación inicial y evaluación del candidato
- **Stage**: Fase 1 y 2 (Implementación y Puerta de Verificación)
- **Prompt / Goal**: Implementar el cambio CR-03, agregar las pruebas correspondientes y correr el arnés determinista de verificación.
- **AI Contribution**: El agente implementó la función auxiliar `_extract_domain` y el soporte de banderas `--domain` y `-d` en la CLI, agregando 16 pruebas y logrando un 99.18% de cobertura y pasando todas las comprobaciones estáticas.
- **Student Decision**: Acepté registrar el commit candidato `c291a00`, pero no asumí que el código estuviera listo únicamente por tener pruebas en verde. Ordené la exportación del diff estricto y la apertura de una sesión limpia de revisión independiente.
- **Impact**: Se obtuvo un candidato trazable y reproducible listo para la auditoría de calidad sin dar por sentado que la alta cobertura garantizaba ausencia de defectos.

## Entry 04 - Revisión independiente: detección de hallazgo crítico y evidencia
- **Stage**: Fase 4 (Reviewer Agent)
- **Prompt / Goal**: Ejecutar un agente revisor en sesión independiente y en modo solo lectura, contrastando el diff contra `review-contract.md`, la especificación y los requisitos.
- **AI Contribution**: El Reviewer Agent analizó minuciosamente el código y detectó un defecto crítico de lógica (RF-01): si un cliente tenía un correo malformado sin arroba y se consultaba con un dominio vacío o solo `@`, la condición de igualdad de cadenas vacías evaluaba verdadero, devolviendo datos erróneos y descartando correos válidos.
- **Student Decision**: Validé la evidencia señalada por el revisor en las líneas 5 a 30 de `src/service.py`, reconociendo que este fallo había eludido al Coder Agent y a la cobertura nominal del 99.18%.
- **Impact**: Se demostró el valor práctico de contar con una segunda mirada independiente capaz de encontrar fallas conceptuales que los arneses de pruebas incompletos no detectan.

## Entry 05 - Decisión humana sobre los hallazgos del Reviewer
- **Stage**: Fase 5 (Human Review Decisions)
- **Prompt / Goal**: Evaluar los seis hallazgos presentados por el revisor independiente y dictar resoluciones vinculantes de ingeniería para cada uno.
- **AI Contribution**: El asistente estructuró el reporte preliminar clasificando las observaciones en tres niveles de severidad (MUST FIX, SHOULD FIX, OPTIONAL).
- **Student Decision**: Tomé la decisión de aceptar únicamente los primeros tres hallazgos (RF-01, RF-02 y RF-03), correspondientes al defecto funcional, la validación de banderas CLI vacías y la adición de pruebas de frontera. Decidí diferir y omitir por el momento las sugerencias opcionales (RF-04 de simplificación sintáctica, RF-05 de reescritura con argparse y RF-06 de historial de commits) para mantener el ciclo acotado y enfocado en la estabilidad del software.
- **Impact**: Quedó patente que la responsabilidad final de qué se corrige y qué se difiere pertenece exclusivamente al criterio humano y no a la aceptación ciega de recomendaciones automáticas.

## Entry 06 - Ciclo de corrección y re-revisión independiente
- **Stage**: Fase 6 y 7 (Fix Cycle y Re-Review)
- **Prompt / Goal**: Ordenar al Coder Agent resolver exclusivamente los hallazgos aceptados, y solicitar una re-evaluación al Reviewer Agent para verificar la solución y descartar regresiones.
- **AI Contribution**: El desarrollador corrigió `_extract_domain` para retornar `None` ante correos malformados, blindó `search_customers` contra dominios vacíos, endureció la validación en la CLI y agregó pruebas de frontera. Posteriormente, el Reviewer Agent confirmó que los tres hallazgos estaban completamente resueltos y dictaminó recomendación favorable para merge sin nuevas regresiones.
- **Student Decision**: Corroboré los resultados del arnés de verificación (40 pruebas pasadas, 99.22% de cobertura y contratos en regla) y firmé formalmente la aprobación en `PR_EVIDENCE.md` como listo para merge.
- **Impact**: Se concluyó el ciclo de ingeniería con trazabilidad total, eliminando la deuda técnica detectada y dejando constancia auditable de cada decisión.
