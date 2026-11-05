import sys
import os

# Para poder ejecutar python src/cli.py directamente desde la raíz
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.service import search_customers


def _parse_cli_args(argv_list: list[str]) -> tuple[str | None, str | None, bool]:
    """
    Parsea los argumentos de la CLI extrayendo el término de búsqueda y el dominio opcional.
    Retorna (term, domain, is_valid).
    """
    term: str | None = None
    domain: str | None = None
    i = 0
    while i < len(argv_list):
        arg = argv_list[i]
        if arg in ("--domain", "-d"):
            if i + 1 < len(argv_list):
                domain = argv_list[i + 1]
                i += 2
            else:
                return None, None, False
        elif arg.startswith("--domain="):
            domain = arg.split("=", 1)[1]
            i += 1
        elif arg.startswith("-d="):
            domain = arg.split("=", 1)[1]
            i += 1
        else:
            if term is None:
                term = arg
            else:
                return None, None, False
            i += 1
    return term, domain, True


def main():
    term, domain, is_valid = _parse_cli_args(sys.argv[1:])

    if not is_valid or term is None:
        print("No se encontraron clientes")
        sys.exit(0)

    # Validaciones
    # VR-01 / AC-01: El término no puede ser vacío y debe contener alfanuméricos
    if not term or not term.strip() or not any(c.isalnum() for c in term):
        print("No se encontraron clientes")
        sys.exit(0)

    # VR-02: El término debe contener al menos 3 caracteres
    if len(term) < 3:
        print("No se encontraron clientes")
        sys.exit(0)

    try:
        if domain is not None:
            results = search_customers(term, domain=domain)
        else:
            results = search_customers(term)

        # EH-01: Sin ninguna coincidencia deberá mostrar el mensaje
        if not results:
            print("No se encontraron clientes")
            sys.exit(0)

        for c in results:
            print(f"[{c.id}] {c.name} {c.last_name} - {c.email}")

    except SystemExit as e:
        # Permitir que el SystemExit de storage.py fluya
        sys.exit(e.code)
    except Exception as e:
        # Prevenir que el usuario vea un stacktrace
        print("Error: Ocurrió un error inesperado en la aplicación.")
        sys.exit(1)


if __name__ == "__main__":
    main()
