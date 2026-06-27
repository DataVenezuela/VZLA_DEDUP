from __future__ import annotations

from scrapers.normalizers.geo import canonical_zone
from scrapers.normalizers.person import name_key, normalize_person_name


def test_geo_variants_resolve_to_same_zone():
    a = canonical_zone("petare")
    b = canonical_zone("PETARE, Miranda")
    c = canonical_zone("Vecinos de Petare reportan falta de agua")
    assert a is not None
    assert a.codigo == "VE-MIR-SUCRE-PETARE"
    assert a.codigo == b.codigo == c.codigo


def test_geo_enriches_latlon():
    zone = canonical_zone("Caracas")
    assert zone is not None
    assert zone.estado == "Distrito Capital"
    assert zone.lat is not None and zone.lon is not None


def test_geo_no_match_returns_none():
    assert canonical_zone("texto sin ubicacion conocida") is None
    assert canonical_zone(None) is None


def test_geo_priority_order():
    # location_text vacío -> usa la descripción.
    zone = canonical_zone("", "se reporta derrumbe en Maracaibo")
    assert zone is not None
    assert zone.codigo == "VE-ZUL-MARACAIBO-MARACAIBO"


def test_person_name_strips_honorifics_and_accents():
    assert normalize_person_name("Sr. José  Pérez") == "jose perez"
    assert normalize_person_name("Dra. María Rodríguez") == "maria rodriguez"


def test_person_name_key_is_order_invariant():
    assert name_key("Jose Perez") == name_key("Perez Jose")
    assert name_key("Jose Perez") == "jose perez"
