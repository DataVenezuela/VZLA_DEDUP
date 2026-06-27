from __future__ import annotations

import json
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from scrapers.normalizers.text import normalize_for_match


_GAZETTEER_PATH = Path(__file__).resolve().parents[1] / "config" / "gazetteer.ve.json"


@dataclass(frozen=True)
class CanonicalZone:
    codigo: str
    estado: str
    municipio: str
    zona: str
    lat: float | None
    lon: float | None

    def as_dict(self) -> dict:
        return {
            "geo_code": self.codigo,
            "geo_zone": self.zona,
            "geo_estado": self.estado,
            "geo_municipio": self.municipio,
            "lat": self.lat,
            "lon": self.lon,
        }


@lru_cache(maxsize=1)
def _alias_index() -> list[tuple[str, CanonicalZone]]:
    """Índice (alias_normalizado, zona) ordenado por alias más largo primero.

    El alias más largo gana => match más específico (ej. "san cristobal" antes que "san")."""
    payload = json.loads(_GAZETTEER_PATH.read_text(encoding="utf-8"))
    index: list[tuple[str, CanonicalZone]] = []
    for entry in payload.get("zonas", []):
        zone = CanonicalZone(
            codigo=entry["codigo"],
            estado=entry["estado"],
            municipio=entry["municipio"],
            zona=entry["zona"],
            lat=entry.get("lat"),
            lon=entry.get("lon"),
        )
        aliases = set(entry.get("alias", []))
        aliases.add(zone.zona)
        for alias in aliases:
            normalized = normalize_for_match(alias)
            if normalized:
                index.append((normalized, zone))
    index.sort(key=lambda item: len(item[0]), reverse=True)
    return index


def _contains_word(haystack: str, needle: str) -> bool:
    """Coincidencia por límite de palabra sobre texto ya normalizado."""
    return re.search(rf"(?:^|\s){re.escape(needle)}(?:\s|$)", haystack) is not None


def canonical_zone(*texts: str | None) -> CanonicalZone | None:
    """Resuelve el primer texto que matchee una zona del gazetteer.

    Acepta varios textos (ej. location_text y luego description) en orden de prioridad.
    Devuelve la zona más específica encontrada, o None si nada matchea."""
    for text in texts:
        normalized = normalize_for_match(text)
        if not normalized:
            continue
        for alias, zone in _alias_index():
            if _contains_word(normalized, alias):
                return zone
    return None
