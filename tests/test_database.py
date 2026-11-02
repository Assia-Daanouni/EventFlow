import pytest

import database
import services


@pytest.fixture
def db(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_NAME", str(tmp_path / "test.db"))
    database.init_db()


def test_reservation_reduces_available_places(db):
    event_id = services.add_event("Atelier Git", "Salle B12", "2026-12-12", 30, 0)
    services.add_reservation(event_id, "Sara Alaoui", "sara@exemple.com", 2)
    assert services.get_event(event_id)["available"] == 28


def test_reservation_refused_when_not_enough_places(db):
    event_id = services.add_event("Atelier Git", "Salle B12", "2026-12-12", 30, 0)
    with pytest.raises(ValueError, match="Places insuffisantes"):
        services.add_reservation(event_id, "Sara Alaoui", "sara@exemple.com", 50)


def test_cancel_frees_places(db):
    event_id = services.add_event("Atelier Git", "Salle B12", "2026-12-12", 30, 0)
    services.add_reservation(event_id, "Sara Alaoui", "sara@exemple.com", 5)
    reservation_id = services.list_reservations()[0]["id"]
    services.cancel_reservation(reservation_id)
    assert services.get_event(event_id)["available"] == 30


def test_cancel_twice_is_refused(db):
    event_id = services.add_event("Atelier Git", "Salle B12", "2026-12-12", 30, 0)
    services.add_reservation(event_id, "Sara Alaoui", "sara@exemple.com", 1)
    reservation_id = services.list_reservations()[0]["id"]
    services.cancel_reservation(reservation_id)
    with pytest.raises(ValueError, match="déjà annulée"):
        services.cancel_reservation(reservation_id)