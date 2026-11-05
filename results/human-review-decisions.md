# Human Review Decisions

## Change
CR-03

### RF-01
- **Reviewer severity**: MUST FIX
- **Human decision**: ACCEPTED
- **Reason**: El defecto señalado es completamente verídico y compromete la integridad del filtrado: si un usuario o sistema suministra un dominio vacío, de solo espacios o con una arroba aislada, `target_domain` se evaluaba como `""` y coincidía exactamente con el `""` que devolvía `_extract_domain` para correos malformados sin arroba, excluyendo además todas las direcciones de correo legítimas. Esto viola de forma directa el criterio de aceptación AC-07.
- **Required action**: Ajustar `_extract_domain` en `src/service.py` para que devuelva `None` cuando el correo carezca de arroba o de nombre de dominio posterior. En `search_customers`, si el parámetro `domain` una vez normalizado queda vacío o sin caracteres de dominio válidos, tratarlo como una consulta que no produce coincidencias (o dominio inválido) y garantizar que jamás coincida con correos sin dominio válido.

### RF-02
- **Reviewer severity**: SHOULD FIX
- **Human decision**: ACCEPTED
- **Reason**: Es necesario mantener consistencia en la interfaz de línea de comandos. Si la CLI rechaza `--domain` sin valor, también debe rechazar sintaxis vacías como `--domain=""`, `-d=""` o valores con solo espacios y arrobas, evitando que lleguen valores no saneados a la capa de servicio.
- **Required action**: Validar en `_parse_cli_args` o `main()` de `src/cli.py` que cualquier valor suministrado para el dominio contenga texto no vacío tras despojar espacios y arrobas. Si es vacío, marcar `is_valid = False` para mostrar `"No se encontraron clientes"` y salir con código `0`.

### RF-03
- **Reviewer severity**: SHOULD FIX
- **Human decision**: ACCEPTED
- **Reason**: La cobertura de código del 99.18% generó una falsa sensación de seguridad al no contemplar valores límite en el nuevo parámetro de dominio, permitiendo que el defecto de RF-01 y la inconsistencia de RF-02 pasaran desapercibidos en las pruebas automatizadas.
- **Required action**: Agregar pruebas unitarias específicas en `tests/test_search.py` para `domain=""`, `domain="   "` y `domain="@"`, así como pruebas en `tests/test_cli.py` para `--domain=""` y `-d=""`.

### RF-04
- **Reviewer severity**: OPTIONAL
- **Human decision**: DEFERRED
- **Reason**: Se omite por el momento para mantener el foco en la corrección funcional y de pruebas sin tocar bifurcaciones accesorias.

### RF-05
- **Reviewer severity**: OPTIONAL
- **Human decision**: DEFERRED
- **Reason**: Migrar el procesador de argumentos a `argparse` está fuera del alcance delimitado de este cambio y podría alterar el comportamiento de la CLI en otros casos de uso.

### RF-06
- **Reviewer severity**: OPTIONAL
- **Human decision**: REJECTED
- **Reason**: La limpieza de los archivos de reporte de actividades anteriores en `results/` responde a la estructura de entrega estipulada en la sección 25 del documento de ADA-09.

## Human Gate
- [x] Return to coder-agent
- [ ] Ready for final re-review
- [ ] Stop / escalate
