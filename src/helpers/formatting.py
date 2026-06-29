from __future__ import annotations

def _fmt(num: float) -> str:
    return f"{num:.2f}".rstrip("0").rstrip(".")
