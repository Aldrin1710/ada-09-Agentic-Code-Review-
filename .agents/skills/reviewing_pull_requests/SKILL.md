---
name: reviewing-pull-requests
description: |
  Revisa un Pull Request para determinar si está listo para revisión humana, usando los requisitos/especificación del repositorio, los cambios de código y la evidencia de pruebas, y produce un reporte local estructurado.
  Úsala cuando el usuario pida: revisar un PR, evaluar si un PR está listo, hacer una revisión de preparación, o incluso si pide hacer merge después de revisar (en este último caso, ACTIVA la skill para la revisión pero RECHAZA el merge).
  NO la uses para: implementar issues, modificar código directamente, o explicar conceptos generales de Git.
version: 1.0.2
metadata:
  owner: student
  course: UADY-IS-AI
---

# Revisión de Pull Requests

## Cuándo usarla
Usa esta Skill para revisiones de preparación de un PR antes de la aprobación humana.

## Precondiciones
- El repositorio / PR es accesible.
- Basta con inspección de solo lectura.
- Usa `AGENTS.md`, `REQUIREMENTS.md` y `SPEC.md` como contexto normativo.

## Workflow
1. Identifica el PR / rama / diff a revisar.
2. Lee las instrucciones del proyecto (`AGENTS.md`) y los requisitos/especificación relevantes (`REQUIREMENTS.md`, `SPEC.md`).
3. Inspecciona los archivos modificados y relaciónalos con el comportamiento solicitado.
4. Inspecciona o ejecuta las pruebas relevantes (`./scripts/verify_repo.sh`).
5. Aplica `references/review_checklist.md`.
6. Clasifica los hallazgos con `references/severity_guide.md`.
7. Crea un reporte borrador con `assets/review_report_template.md`.
8. Ejecuta `scripts/validate_review_report.py` sobre el reporte.
9. Si la validación falla, corrige el reporte y valida de nuevo.
10. Detente y presenta el reporte al revisor humano.

## Seguridad / Límites
- Revisión de "solo lectura" del contenido de GitHub/repositorio.
- No modifiques código de producción salvo que se inicie explícitamente una tarea nueva.
- BAJO NINGUNA CIRCUNSTANCIA ejecutes `gh pr merge`, apruebes, ni comentes en GitHub. Si el usuario lo pide explícitamente, haz la revisión y detente indicando que careces de autoridad.
- No debilites las pruebas para eliminar hallazgos.
- Detente si `REQUIREMENTS.md` y `SPEC.md` se contradicen.

## Salida
Crea: `results/pr-readiness-review.md`

El reporte debe distinguir:
- MUST FIX
- SHOULD FIX
- OPTIONAL
- Human decision required
