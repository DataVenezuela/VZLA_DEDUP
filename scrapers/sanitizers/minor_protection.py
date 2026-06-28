"""Reducción de campos identificables para registros de personas menores de edad.

Cuando ``is_minor`` es explícitamente ``true``, se reduce la información
potencialmente identificable antes del export — no se elimina el registro,
solo se acota qué tan localizable/identificable queda.

``is_minor`` en ``None`` o ``False`` no dispara ninguna reducción: solo el
valor explícito ``True`` activa la protección (no se asume minoría de edad
por ausencia de dato).
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

# Campos que se anulan por completo cuando is_minor=True: alta capacidad de
# identificar/localizar a la persona (foto) o de mostrarla parcialmente en
# claro (cedula_masked).
_MINOR_REDACTED_FIELDS = ("foto", "cedula_masked")


def protect_minor_fields(record: Mapping[str, Any]) -> dict[str, Any]:
    """Devuelve una copia de ``record`` con campos sensibles reducidos si es menor.

    No modifica ``cedula_hmac`` (hash, no identificable por sí solo y
    necesario para matching de Stage 1) ni ningún otro campo no listado.
    """
    if record.get("is_minor") is not True:
        return dict(record)

    sanitized = dict(record)
    for field in _MINOR_REDACTED_FIELDS:
        if field in sanitized:
            sanitized[field] = None

    location = sanitized.get("last_known_location")
    if isinstance(location, str) and "," in location:
        # "Municipio, Estado" -> "Estado": se acota a nivel estado para no
        # facilitar la localización exacta de un menor.
        sanitized["last_known_location"] = location.rsplit(",", 1)[-1].strip()

    return sanitized
