import pytest
import services


@pytest.mark.parametrize("available, requested, expected", [
    (10, 4, True),
    (5, 5, True),
    (3, 4, False),
    (10, 0, False),
])
def test_has_enough_places(available, requested, expected):
    assert services.has_enough_places(available, requested) == expected


def test_calculate_total():
    assert services.calculate_total(50, 3) == 150


def test_calculate_total_zero_places():
    with pytest.raises(ValueError):
        services.calculate_total(50, 0)


def test_validate_event_ok():
    services.validate_event("Conférence", "ENSA", "2026-12-05", 100, 50)


def test_validate_event_empty_title():
    with pytest.raises(ValueError):
        services.validate_event(" ", "ENSA", "2026-12-05", 100, 50)


def test_validate_event_zero_capacity():
    with pytest.raises(ValueError):
        services.validate_event("Conférence", "ENSA", "2026-12-05", 0, 50)


def test_validate_event_negative_price():
    with pytest.raises(ValueError):
        services.validate_event("Conférence", "ENSA", "2026-12-05", 100, -1)


@pytest.mark.parametrize("email, expected", [
    ("sara@exemple.com", True),
    ("sara.exemple.com", False),
    ("sara@", False),
    (None, False),
])
def test_is_valid_email(email, expected):
    assert services.is_valid_email(email) == expected