# PR Evidence

## Change
- **Change ID**: CR-03
- **PR / Branch**: `ada09/cr-email-domain-filter`
- **Base commit**: `801ec04`
- **Final commit**: `c63f51f`

## Requirements / Acceptance Criteria
- **FR-02**: Evaluación del término de búsqueda en los campos permitidos (`name`, `last_name`, `email`).
- **FR-03**: Coincidencias parciales y por prefijo en los campos permitidos.
- **FR-04**: Búsqueda insensible a mayúsculas y minúsculas.
- **FR-05**: Ordenamiento determinista (exactas por ID ascendente, luego parciales por apellido e ID).
- **FR-07**: Parámetro opcional de filtrado por dominio de correo (`domain: str | None = None`) en `search_customers` y soporte en CLI mediante `--domain` / `-d`.
- **AC-07**: Cuando se especifica un dominio, los resultados deben incluir únicamente clientes cuyo correo pertenezca a dicho dominio de forma estricta (insensible a mayúsculas y tolerante a prefijo `@`), preservando el comportamiento previo cuando el filtro no se suministra.

## Implementation
- **Coder report**: `results/coder-report.md`
- **Files changed**:
  - `src/service.py`
  - `src/cli.py`
  - `tests/test_search.py`
  - `tests/test_cli.py`
  - `docs/traceability.md`
- **Commits**:
  - `c291a00`: `feat: implement CR-03`
  - `c63f51f`: `fix(review): resolve findings RF-01, RF-02, and RF-03`

## Verification
- **Verification command**: `bash scripts/verify_repo.sh`
- **Final result**: `VERIFY_REPO: PASS` (código de salida 0)
- **Tests**: 40 pasadas, 0 fallidas en 0.68s
- **Code coverage**: 99.22% (umbral obligatorio >= 90.00%)
  - `src/service.py`: 100%
  - `src/storage.py`: 100%
  - `src/model.py`: 100%
  - `src/cli.py`: 98%
- **Static compilation**: `python -m compileall src tests` (0 errores, 0 advertencias)
- **Security / repo checks**: `REPO_CONTRACT: PASS` (`python scripts/check_repo_contract.py`)

## Independent Review
- **Review report**: `results/review-report.md`
- **MUST FIX found**: 1 (RF-01: defecto de filtrado al suministrar dominios vacíos o con solo `@` que coincidían con correos sin `@`)
- **SHOULD FIX found**: 2 (RF-02: inconsistencia en validación de banderas CLI vacías; RF-03: omisión de pruebas de frontera)
- **OPTIONAL found**: 3 (RF-04: llamada redundante con `if/else`; RF-05: analizador manual de argumentos; RF-06: limpieza de reportes de asignaciones pasadas)

## Human Decisions
- **Accepted**: RF-01, RF-02, RF-03
- **Modified**: 0
- **Rejected**: RF-06
- **Deferred**: RF-04, RF-05
- **Documento de decisiones**: `results/human-review-decisions.md`

## Re-review
- **Resolved**: 3 (RF-01, RF-02, RF-03)
- **Partially resolved**: 0
- **Not resolved**: 0
- **New MUST FIX**: 0
- **Re-review report**: `results/re-review-report.md`

## Traceability

| Requirement / AC | Task / Change | Code | Test | Review Finding |
|---|---|---|---|---|
| FR-07 / AC-07 | Filtrado opcional por dominio en servicio | `src/service.py` (`search_customers`) | `tests/test_search.py` (`test_search_with_email_domain_filter`) | RF-01 (Resuelto) |
| FR-07 / AC-07 | Normalización de prefijo `@` | `src/service.py` (`_extract_domain`) | `tests/test_search.py` (`test_search_domain_with_at_prefix`) | RF-01 (Resuelto) |
| FR-07 / AC-07 | Insensibilidad a mayúsculas | `src/service.py` (`search_customers`) | `tests/test_search.py` (`test_search_domain_case_insensitive`) | RF-03 (Resuelto) |
| FR-07 / AC-07 | Preservación del ordenamiento determinista | `src/service.py` (`search_customers`) | `tests/test_search.py` (`test_search_domain_preserves_ordering`) | Ninguno |
| FR-07 / AC-07 | Manejo seguro de correos malformados y filtro vacío | `src/service.py` (`_extract_domain`) | `tests/test_search.py` (`test_search_domain_empty_or_whitespace_or_only_at`) | RF-01, RF-03 (Resueltos) |
| FR-07 / AC-07 | Banderas CLI `--domain` y `-d` | `src/cli.py` (`_parse_cli_args`) | `tests/test_cli.py` (`test_cli_domain_long_flag`, `test_cli_domain_short_flag`) | RF-02 (Resuelto) |
| FR-07 / AC-07 | Validación de banderas vacías (`--domain=""`) | `src/cli.py` (`_parse_cli_args`) | `tests/test_cli.py` (`test_cli_domain_empty_or_invalid_values`) | RF-02, RF-03 (Resueltos) |
| FR-02..FR-05 | Compatibilidad hacia atrás (`domain=None`) | `src/service.py` (`search_customers`) | `tests/test_search.py` (`test_search_domain_none_backward_compatible`) | Ninguno |

## Remaining Risks / Technical Debt
- **Analizador de argumentos manual (RF-05 diferido)**: El ciclo `while` en `src/cli.py` cumple satisfactoriamente los requerimientos actuales y fue blindado contra argumentos vacíos, pero si la aplicación requiere opciones más avanzadas en el futuro, convendrá migrar a `argparse`.
- **Bifurcación redundante en CLI (RF-04 diferido)**: Se conserva la llamada condicional en `src/cli.py` sin impacto en la funcionalidad; representa una oportunidad menor de refactorización cosmética.

## Final Human Decision
- [ ] NOT READY
- [x] READY FOR HUMAN MERGE

Approved by: Aldrin (User)  
Date: 2026-11-05
