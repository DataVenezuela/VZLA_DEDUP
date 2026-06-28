from __future__ import annotations

from scrapers.sanitizers.minor_protection import protect_minor_fields


def _record(**overrides: object) -> dict:
    base = {
        "full_name": "Juan Demo Perez",
        "foto": "https://example.org/foto.jpg",
        "cedula_hmac": "a" * 64,
        "cedula_masked": "V-****5821",
        "last_known_location": "Iribarren, Lara",
        "is_minor": True,
    }
    base.update(overrides)
    return base


def test_minor_record_redacts_foto_and_cedula_masked():
    sanitized = protect_minor_fields(_record())
    assert sanitized["foto"] is None
    assert sanitized["cedula_masked"] is None


def test_minor_record_keeps_cedula_hmac_for_matching():
    sanitized = protect_minor_fields(_record())
    assert sanitized["cedula_hmac"] == "a" * 64


def test_minor_record_coarsens_location_to_estado():
    sanitized = protect_minor_fields(_record())
    assert sanitized["last_known_location"] == "Lara"


def test_minor_record_location_without_comma_is_unchanged():
    sanitized = protect_minor_fields(_record(last_known_location="Lara"))
    assert sanitized["last_known_location"] == "Lara"


def test_minor_record_with_none_location_is_unchanged():
    sanitized = protect_minor_fields(_record(last_known_location=None))
    assert sanitized["last_known_location"] is None


def test_non_minor_record_is_untouched():
    for is_minor in (False, None):
        record = _record(is_minor=is_minor)
        sanitized = protect_minor_fields(record)
        assert sanitized == record


def test_record_without_is_minor_key_is_untouched():
    """Event/AcopioCenter dicts never have is_minor — must pass through as-is."""
    record = {"name": "Centro Demo", "foto": "x"}
    assert protect_minor_fields(record) == record


def test_returns_copy_not_same_object():
    record = _record(is_minor=False)
    sanitized = protect_minor_fields(record)
    assert sanitized is not record
