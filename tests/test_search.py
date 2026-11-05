import pytest
from unittest.mock import patch
from src.model import Customer
from src.service import search_customers

@pytest.fixture
def mock_customers():
    return [
        Customer(id=1, name="Alejandro", last_name="Zavala", email="ale.zavala@example.com"),
        Customer(id=2, name="Ale", last_name="Perez", email="contacto@ale.com"),
        Customer(id=3, name="Maria", last_name="Gomez", email="maria@ale.com"),
        Customer(id=4, name="Pedro", last_name="Alejandro", email="pedro@test.com")
    ]

@patch('src.service.load_customers')
def test_search_exact_and_partial_order(mock_load, mock_customers):
    # TS-03 y TS-04 ordenamiento
    mock_load.return_value = mock_customers

    results = search_customers("ale")

    assert len(results) == 4
    # Coincidencia exacta "ale" en nombre (id=2) va primero
    assert results[0].id == 2

    # Las parciales se ordenan por apellido: Alejandro (4), Gomez (3), Zavala (1)
    assert results[1].id == 4
    assert results[2].id == 3
    assert results[3].id == 1

@patch('src.service.load_customers')
def test_search_case_insensitive(mock_load, mock_customers):
    # TS-03: Término minúsculas (o viceversa) devuelve cliente de forma insensible
    mock_load.return_value = mock_customers

    # Aunque la búsqueda es en mayúsculas, debe encontrar a "Ale" y a los demás
    results = search_customers("ALE")

    assert len(results) == 4
    assert results[0].id == 2

@patch('src.service.load_customers')
def test_search_unallowed_fields(mock_load, mock_customers):
    # TS-02: Búsqueda que coincida únicamente con campos no permitidos no devuelve resultados
    # Simulamos buscar "555" (un teléfono)
    mock_load.return_value = mock_customers
    results = search_customers("5551234")
    assert len(results) == 0

@patch('src.service.load_customers')
def test_search_no_results(mock_load, mock_customers):
    # Parte de TS-06: Sin coincidencia
    mock_load.return_value = mock_customers

    results = search_customers("invento")
    assert len(results) == 0

@patch('src.service.load_customers')
def test_search_exact_match_last_name(mock_load):
    # CR-02: Coincidencia exacta en last_name (insensible a mayúsculas/minúsculas) se prioriza antes que parciales
    mock_load.return_value = [
        Customer(id=1, name="Carlos", last_name="Perezosa", email="carlos@example.com"),
        Customer(id=2, name="Lucia", last_name="Perez", email="lucia@example.com"),
        Customer(id=3, name="Perezoso", last_name="Alvarez", email="perezoso@example.com"),
    ]

    results = search_customers("pErEz")

    assert [c.id for c in results] == [2, 3, 1]

@patch('src.service.load_customers')
def test_search_deterministic_tie_breaking_by_id(mock_load):
    # CR-02: Desempate determinista por id ascendente en coincidencias exactas y en parciales con mismo apellido
    mock_load.return_value = [
        Customer(id=10, name="Alex", last_name="Gomez", email="alex10@example.com"),
        Customer(id=4, name="Bruno", last_name="Alex", email="bruno4@example.com"),
        Customer(id=7, name="Alex", last_name="Zavala", email="alex7@example.com"),
        Customer(id=9, name="Alexia", last_name="Lopez", email="alexia9@example.com"),
        Customer(id=3, name="Alexander", last_name="Lopez", email="alexander3@example.com"),
        Customer(id=6, name="Alexis", last_name="Alpha", email="alexis6@example.com"),
    ]

    results = search_customers("alex")

    # Exactas ordenadas por id ascendente: 4, 7, 10
    # Parciales ordenadas por apellido (Alpha -> 6, Lopez -> 3 luego 9)
    assert [c.id for c in results] == [4, 7, 10, 6, 3, 9]

@patch('src.service.load_customers')
def test_search_with_email_domain_filter(mock_load):
    # CR-03 / AC-07: Filtrado por dominio de correo específico
    mock_load.return_value = [
        Customer(id=1, name="Carlos", last_name="Perez", email="carlos@example.com"),
        Customer(id=2, name="Carlos", last_name="Gomez", email="carlos@other.com"),
        Customer(id=3, name="Ana", last_name="Perez", email="ana@example.com"),
    ]

    results = search_customers("Carlos", domain="example.com")

    assert len(results) == 1
    assert results[0].id == 1
    assert results[0].email == "carlos@example.com"

@patch('src.service.load_customers')
def test_search_domain_with_at_prefix(mock_load):
    # CR-03 / AC-07: Dominio proporcionado con prefijo '@'
    mock_load.return_value = [
        Customer(id=1, name="Carlos", last_name="Perez", email="carlos@example.com"),
        Customer(id=2, name="Carlos", last_name="Gomez", email="carlos@other.com"),
    ]

    results = search_customers("Carlos", domain="@example.com")

    assert len(results) == 1
    assert results[0].id == 1

@patch('src.service.load_customers')
def test_search_domain_case_insensitive(mock_load):
    # CR-03 / AC-07 / FR-04: Comparación de dominio insensible a mayúsculas/minúsculas
    mock_load.return_value = [
        Customer(id=1, name="Carlos", last_name="Perez", email="carlos@ExAmPlE.com"),
        Customer(id=2, name="Carlos", last_name="Gomez", email="carlos@OTHER.COM"),
    ]

    results = search_customers("Carlos", domain="EXAMPLE.COM")

    assert len(results) == 1
    assert results[0].id == 1

@patch('src.service.load_customers')
def test_search_domain_no_match(mock_load):
    # CR-03 / AC-07: Búsqueda con término coincidente pero dominio no existente retorna lista vacía
    mock_load.return_value = [
        Customer(id=1, name="Carlos", last_name="Perez", email="carlos@example.com"),
    ]

    results = search_customers("Carlos", domain="nonexistent.com")

    assert results == []

@patch('src.service.load_customers')
def test_search_domain_preserves_ordering(mock_load):
    # CR-03 / FR-05 / AC-04: El filtro de dominio conserva el orden de exactas por id y parciales por apellido/id
    mock_load.return_value = [
        Customer(id=10, name="Alex", last_name="Zavala", email="alex10@example.com"),
        Customer(id=2, name="Alex", last_name="Alvarez", email="alex2@example.com"),
        Customer(id=1, name="Alex", last_name="Abe", email="alex1@other.com"),
        Customer(id=5, name="Alexander", last_name="Beta", email="alexander5@example.com"),
        Customer(id=4, name="Alexia", last_name="Alpha", email="alexia4@example.com"),
    ]

    results = search_customers("alex", domain="example.com")

    # Coincidencias exactas con dominio example.com: id=2, id=10
    # Coincidencias parciales con dominio example.com: id=4 (Alpha), id=5 (Beta)
    assert [c.id for c in results] == [2, 10, 4, 5]

@patch('src.service.load_customers')
def test_search_domain_none_backward_compatible(mock_load, mock_customers):
    # CR-03: Compatibilidad 100% hacia atrás cuando domain es None o no se pasa
    mock_load.return_value = mock_customers

    results_default = search_customers("ale")
    results_explicit_none = search_customers("ale", domain=None)

    assert results_default == results_explicit_none
    assert len(results_default) == 4

@patch('src.service.load_customers')
def test_search_domain_email_without_at_symbol(mock_load):
    # Cliente con email sin arroba es excluido cuando se filtra por dominio
    mock_load.return_value = [
        Customer(id=1, name="Carlos", last_name="Perez", email="carlos_sin_arroba"),
    ]
    results = search_customers("Carlos", domain="example.com")
    assert results == []



