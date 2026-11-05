from src.model import Customer
from src.storage import load_customers


def _extract_domain(email: str) -> str | None:
    """Extrae el dominio de una dirección de correo en minúsculas, o None si no es válido."""
    if "@" in email:
        domain = email.rsplit("@", 1)[1].strip().lower()
        if domain:
            return domain
    return None


def search_customers(term: str, domain: str | None = None) -> list[Customer]:
    """
    Filtra y ordena los clientes basados en un término de búsqueda y un dominio de correo opcional.
    """
    customers = load_customers('data/customers.json')
    term_lower = term.lower()

    target_domain: str | None = None
    if domain is not None:
        target_domain = domain.strip().lower().lstrip('@')
        if not target_domain:
            return []

    exact_matches: list[Customer] = []
    partial_matches: list[Customer] = []

    for customer in customers:
        if target_domain is not None:
            cust_domain = _extract_domain(customer.email)
            if cust_domain is None or cust_domain != target_domain:
                continue

        name_lower = customer.name.lower()
        last_name_lower = customer.last_name.lower()
        email_lower = customer.email.lower()

        # Coincidencia exacta por nombre, apellido o correo
        is_exact = (
            term_lower == name_lower
            or term_lower == last_name_lower
            or term_lower == email_lower
        )

        if is_exact:
            exact_matches.append(customer)
            continue

        # Coincidencia parcial en nombre, apellido o correo
        if (term_lower in name_lower or
            term_lower in last_name_lower or
            term_lower in email_lower):
            partial_matches.append(customer)

    # Ordenar coincidencias exactas por id ascendente
    exact_matches.sort(key=lambda c: c.id)

    # Ordenar coincidencias parciales alfabéticamente por apellido y desempatar por id ascendente
    partial_matches.sort(key=lambda c: (c.last_name.lower(), c.id))

    # Retornar primero exactas, luego parciales
    return exact_matches + partial_matches
