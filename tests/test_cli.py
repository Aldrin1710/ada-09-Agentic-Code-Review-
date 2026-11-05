import pytest
import sys
from unittest.mock import patch
from src.cli import main

def run_cli_internal(capsys, *args):
    with patch.object(sys, 'argv', ['src/cli.py'] + list(args)):
        try:
            main()
        except SystemExit as e:
            return e.code, capsys.readouterr().out
    return 0, capsys.readouterr().out

def test_cli_empty_term(capsys):
    # TS-01 y TS-04: Búsqueda vacía es rechazada
    code, out = run_cli_internal(capsys, "")
    assert "No se encontraron clientes" in out
    assert code == 0

def test_cli_short_term(capsys):
    # TS-05: Al menos 3 caracteres
    code, out = run_cli_internal(capsys, "al")
    assert "No se encontraron clientes" in out
    assert code == 0

def test_cli_non_alphanumeric(capsys):
    # TS-01: Caracteres no alfanuméricos
    code, out = run_cli_internal(capsys, "@@@")
    assert "No se encontraron clientes" in out
    assert code == 0

def test_cli_valid_term(capsys):
    code, out = run_cli_internal(capsys, "ale")
    assert "Alejandro" in out
    assert "Maria" not in out
    assert code is None or code == 0

def test_cli_no_match(capsys):
    # TS-06: Mensaje de error (no se encontraron) para un cliente inexistente
    code, out = run_cli_internal(capsys, "terminoinexistente")
    assert "No se encontraron clientes" in out
    assert code == 0

@patch('src.cli.search_customers')
def test_cli_unexpected_error(mock_search, capsys):
    mock_search.side_effect = Exception("Unexpected")
    code, out = run_cli_internal(capsys, "ale")
    assert "Ocurrió un error inesperado" in out
    assert code == 1

@patch('src.cli.search_customers')
def test_cli_system_exit_passthrough(mock_search, capsys):
    mock_search.side_effect = SystemExit(3)
    code, out = run_cli_internal(capsys, "ale")
    assert code == 3

def test_cli_domain_long_flag(capsys):
    # CR-03 / AC-07: Argumento --domain filtra clientes por dominio
    code, out = run_cli_internal(capsys, "ana", "--domain", "example.com")
    assert "Ana Perez" in out
    assert "Carlos Bustamante" not in out
    assert code == 0

def test_cli_domain_short_flag(capsys):
    # CR-03: Argumento -d filtra clientes por dominio
    code, out = run_cli_internal(capsys, "ana", "-d", "mail.com")
    assert "Carlos Bustamante" in out
    assert "Ana Perez" not in out
    assert code == 0

def test_cli_domain_with_at_prefix(capsys):
    # CR-03: Argumento de dominio con prefijo '@'
    code, out = run_cli_internal(capsys, "ana", "-d", "@example.com")
    assert "Ana Perez" in out
    assert "Carlos Bustamante" not in out
    assert code == 0

def test_cli_domain_case_insensitive(capsys):
    # CR-03: Dominio insensible a mayúsculas
    code, out = run_cli_internal(capsys, "ana", "--domain", "EXAMPLE.COM")
    assert "Ana Perez" in out
    assert code == 0

def test_cli_domain_no_match(capsys):
    # CR-03: Búsqueda con dominio sin coincidencias
    code, out = run_cli_internal(capsys, "ana", "--domain", "nonexistent.com")
    assert "No se encontraron clientes" in out
    assert code == 0

def test_cli_domain_flag_missing_value(capsys):
    # CR-03: Flag de dominio sin valor
    code, out = run_cli_internal(capsys, "ana", "--domain")
    assert "No se encontraron clientes" in out
    assert code == 0

def test_cli_domain_flag_before_term(capsys):
    # CR-03: Flag de dominio antes del término
    code, out = run_cli_internal(capsys, "--domain", "example.com", "ana")
    assert "Ana Perez" in out
    assert code == 0

def test_cli_domain_equals_syntax(capsys):
    # CR-03: Sintaxis con signo igual --domain=val y -d=val
    code1, out1 = run_cli_internal(capsys, "ana", "--domain=example.com")
    assert "Ana Perez" in out1
    assert code1 == 0

    code2, out2 = run_cli_internal(capsys, "ana", "-d=mail.com")
    assert "Carlos Bustamante" in out2
    assert code2 == 0

def test_cli_unexpected_extra_argument(capsys):
    # Argumento extra inesperado es rechazado de forma segura
    code, out = run_cli_internal(capsys, "ana", "extra_term")
    assert "No se encontraron clientes" in out
    assert code == 0


