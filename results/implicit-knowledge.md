# Conocimiento Implícito Detectado (`Implicit Knowledge Found`)

## IK-01
- **Qué era (`What`)**:
  El archivo fuente de verdad de requisitos se llama en realidad `REQUERIMENTS.md` (con error ortográfico) en lugar de `REQUIREMENTS.md` como lo referencian `AGENTS.md` y `TASK_UNDER_TEST.md`.
- **Cómo se descubrió (`How was it discovered`)**:
  Ejecutando `Get-ChildItem -Force` en la raíz del repositorio antes de intentar leer `REQUIREMENTS.md`.
- **¿Debería permanecer implícito? (`Should this remain implicit?`)**:
  NO
- **Dónde debe hacerse explícito (`Where should it become explicit?`)**:
  Renombrar el archivo a `REQUIREMENTS.md` y validar su existencia de forma determinista mediante `scripts/check_repo_contract.py` y `AGENTS.md`.

## IK-02
- **Qué era (`What`)**:
  Los archivos de bytecode compilado (`src/__pycache__/*.pyc`, `tests/__pycache__/*.pyc`) y `.coverage` están rastreados por error en Git, por lo que ejecutar `pytest --cov=src` contamina `git status` con cambios binarios fuera de alcance.
- **Cómo se descubrió (`How was it discovered`)**:
  Únicamente después de ejecutar `pytest -v --cov=src tests/; git status -s` al final de la corrida BEFORE.
- **Riesgo (`Risk`)**:
  El agente modifica artefactos binarios no relacionados en cada ejecución de pruebas, violando el Definition of Done (*"No unrelated files are changed"*) y generando conflictos de fusión.
- **Remediación (`Remediation`)**:
  Eliminar `__pycache__/` y `.coverage` del índice de Git (`git rm --cached`), agregar `.gitignore`, e incluir un guardrail determinista en `scripts/check_repo_contract.py` que falle si cualquier archivo `.pyc`, `__pycache__` o `.coverage` está rastreado en Git.

## IK-03
- **Qué era (`What`)**:
  El punto de entrada real de la CLI es `src/cli.py` (o `search.bat` en Windows), NO `search.py` como afirma `ARCHITECTURE.md` (`python search.py "termino"`), y las validaciones de entrada (`VR-01`, `VR-02`) viven en `src/cli.py` mientras que la salida por error de esquema JSON (`EH-02`) vive en `src/storage.py`.
- **Cómo se descubrió (`How was it discovered`)**:
  Leyendo los 4 archivos dentro de `src/` (`cli.py`, `service.py`, `storage.py`, `model.py`) y comparándolos contra `ARCHITECTURE.md` y `README.md`.
- **Riesgo (`Risk`)**:
  Un agente que confíe en `ARCHITECTURE.md` buscará un archivo `search.py` inexistente o colocará la lógica de validación/búsqueda en el módulo equivocado.
- **Remediación (`Remediation`)**:
  Actualizar `ARCHITECTURE.md` para reflejar los límites reales de cada módulo y crear `docs/REPO_MAP.md` con los puntos de entrada exactos, responsabilidades por capa y una Guía de Cambios paso a paso.

## IK-04
- **Qué era (`What`)**:
  Ejecutar la medición de cobertura y verificar `NFR-03` (mínimo 90% de cobertura + verificación estática de tipos/sintaxis) requiere comandos específicos (`pytest --cov=src --cov-fail-under=90` y chequeos de contrato/compilación) que no aparecen en `AGENTS.md`.
- **Cómo se descubrió (`How was it discovered`)**:
  Cruzando manualmente la información de `README.md` (`pytest --cov=src tests/`), `REQUERIMENTS.md` (`NFR-03`) y `pytest.ini`.
- **¿Debería permanecer implícito? (`Should this remain implicit?`)**:
  NO
- **Dónde debe hacerse explícito (`Where should it become explicit?`)**:
  En `AGENTS.md` (sección `Standard Commands`), `scripts/verify_repo.sh` (y `scripts/verify_repo.ps1`), y `.github/workflows/verify.yml`.

## IK-05
- **Qué era (`What`)**:
  `data/customers.json` es el dataset semilla utilizado por las pruebas de integración de la CLI (`test_cli_valid_term` en `tests/test_cli.py`), y no debe modificarse al agregar pruebas unitarias (las pruebas unitarias en `tests/test_search.py` deben usar mocks sobre `src.service.load_customers`).
- **Cómo se descubrió (`How was it discovered`)**:
  Inspeccionando `tests/test_search.py`, `tests/test_cli.py` y `data/customers.json`.
- **Riesgo (`Risk`)**:
  Un agente podría editar `data/customers.json` para probar casos borde, rompiendo las pruebas existentes de la CLI o alterando los datos semilla.
- **Remediación (`Remediation`)**:
  Documentar `data/customers.json` bajo `Do Not Edit Directly` en `docs/REPO_MAP.md` y `AGENTS.md`, e implementar una verificación determinista con `git diff` sobre `data/customers.json` dentro de `scripts/check_repo_contract.py`.
