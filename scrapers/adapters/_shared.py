"""
scrapers/adapters/_shared.py
=============================
Helpers internos compartidos por los adapters del pipeline: timestamp UTC,
hashing de contenido para ``RawContent.content_hash`` y backoff exponencial
con jitter para reintentos.

No es parte de ``AdapterProtocol`` (ver ``base.py``) — son utilidades de
implementacion para que cada adapter no reinvente la misma logica.
"""

from __future__ import annotations

import hashlib
import random
import time
from collections.abc import Callable
from datetime import datetime, timezone


def now_utc() -> str:
    """Timestamp ISO-8601 UTC sin microsegundos, para ``fetched_at``."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_hex(data: bytes) -> str:
    """SHA-256 hexadecimal con el prefijo ``sha256:`` que usa ``content_hash``."""
    return f"sha256:{hashlib.sha256(data).hexdigest()}"


def backoff_delay(attempt: int, *, base: float = 1.0, max_delay: float = 60.0) -> float:
    """
    Exponential backoff con jitter completo.

    ``attempt`` empieza en 1.  Formula:
        delay = min(base * 2^(attempt-1), max_delay) + random(0, 1)
    """
    exp: float = base * (2 ** (attempt - 1))
    capped: float = min(exp, max_delay)
    return capped + random.random()


class RateLimiter:
    """Rate limiter de ventana deslizante para requests por fuente.

    Se usa en adapters paginados para respetar `rate_limit_per_minute` sin
    acoplar la lógica al transport de httpx. El reloj y sleep son inyectables
    para que los tests no esperen tiempo real.
    """

    def __init__(
        self,
        max_calls: int,
        *,
        window_seconds: float = 60.0,
        clock: Callable[[], float] = time.monotonic,
        sleeper: Callable[[float], None] = time.sleep,
    ) -> None:
        if max_calls < 1:
            raise ValueError("max_calls must be a positive integer")
        if window_seconds <= 0:
            raise ValueError("window_seconds must be positive")
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self._clock = clock
        self._sleeper = sleeper
        self._calls: list[float] = []

    def wait(self) -> None:
        """Bloquea hasta que haya cupo para una llamada en la ventana actual."""
        while True:
            now = self._clock()
            self._calls = [
                ts for ts in self._calls
                if now - ts < self.window_seconds
            ]
            if len(self._calls) < self.max_calls:
                self._calls.append(now)
                return

            wait_for = self.window_seconds - (now - self._calls[0])
            self._sleeper(max(wait_for, 0.0))
