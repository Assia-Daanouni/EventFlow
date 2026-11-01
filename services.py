import database

# ---------- Règles métier pures (faciles à tester) ----------


def validate_event(title, location, event_date, capacity, price):
    if not title or not title.strip():
        raise ValueError("Le titre est obligatoire")
    if not location or not location.strip():
        raise ValueError("Le lieu est obligatoire")
    if not event_date:
        raise ValueError("La date est obligatoire")
    if capacity <= 0:
        raise ValueError("La capacité doit être supérieure à zéro")
    if price < 0:
        raise ValueError("Le prix ne peut pas être négatif")


def is_valid_email(email):
    if not email or " " in email:
        return False
    local, _, domain = email.strip().partition("@")
    return (bool(local) and "@" not in domain and "." in domain
            and not domain.startswith(".") and not domain.endswith("."))


def has_enough_places(available, requested):
    return 0 < requested <= available


def calculate_total(price, places):
    if places <= 0:
        raise ValueError("Le nombre de places doit être supérieur à zéro")
    return price * places


def to_int(value, label):
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ValueError(f"{label} doit être un nombre entier")


def to_float(value, label):
    try:
        return float(str(value).replace(",", "."))
    except ValueError:
        raise ValueError(f"{label} doit être un nombre")


# ---------- Événements ----------
# places libres = capacité - somme des places des réservations ACTIVE
EVENT_SELECT = """
    SELECT e.*,
           e.capacity - COALESCE(SUM(CASE WHEN r.status = 'ACTIVE' THEN r.places END), 0) AS available
    FROM events e
    LEFT JOIN reservations r ON r.event_id = e.id
"""


def list_events():
    return database.query(EVENT_SELECT + " GROUP BY e.id ORDER BY e.event_date")


def get_event(event_id):
    return database.query_one(EVENT_SELECT + " WHERE e.id = ? GROUP BY e.id", (event_id,))


def add_event(title, location, event_date, capacity, price):
    capacity = to_int(capacity, "La capacité")
    price = to_float(price, "Le prix")
    validate_event(title, location, event_date, capacity, price)
    new_id, _ = database.execute(
        "INSERT INTO events (title, location, event_date, capacity, price) VALUES (?, ?, ?, ?, ?)",
        (title.strip(), location.strip(), event_date, capacity, price))
    return new_id


def delete_event(event_id):
    if get_event(event_id) is None:
        raise ValueError("Événement introuvable")
    database.execute("DELETE FROM events WHERE id = ?", (event_id,))


# ---------- Réservations ----------


def list_reservations():
    return database.query("""
        SELECT r.id, r.full_name, r.email, r.places, r.status,
               e.title AS event_title, e.price * r.places AS total
        FROM reservations r
        JOIN events e ON e.id = r.event_id
        ORDER BY r.id DESC
    """)


def add_reservation(event_id, full_name, email, places):
    places = to_int(places, "Le nombre de places")
    if not full_name or not full_name.strip():
        raise ValueError("Le nom est obligatoire")
    if not is_valid_email(email):
        raise ValueError("Adresse email invalide")
    event = get_event(event_id)
    if event is None:
        raise ValueError("Événement introuvable")
    total = calculate_total(event["price"], places)
    if not has_enough_places(event["available"], places):
        raise ValueError(f"Places insuffisantes : il reste {event['available']} place(s)")
    database.execute(
        "INSERT INTO reservations (event_id, full_name, email, places) VALUES (?, ?, ?, ?)",
        (event_id, full_name.strip(), email.strip().lower(), places))
    return total


def cancel_reservation(reservation_id):
    _, changed = database.execute(
        "UPDATE reservations SET status = 'CANCELLED' WHERE id = ? AND status = 'ACTIVE'",
        (reservation_id,))
    if changed == 0:
        raise ValueError("Réservation introuvable ou déjà annulée")