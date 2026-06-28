"""
scrapers/adapters/base.py
=========================
Contrato común (Protocol) que deben cumplir todos los adapters del pipeline.
"""
from __future__ import annotations

from typing import Any, Iterator, Protocol, runtime_checkable

RawContent = dict[str, Any]


@runtime_checkable
class AdapterProtocol(Protocol):
    """Interfaz que todo adapter del pipeline debe implementar."""

    def fetch(self, url: str, **kwargs: Any) -> RawContent:
        ...

    def fetch_all(self, url: str, **kwargs: Any) -> Iterator[RawContent]:
        ...
