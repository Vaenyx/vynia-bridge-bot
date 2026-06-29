from __future__ import annotations

def stars_from_xp(xp: int) -> float:
    prestiges = xp // 487000
    xp %= 487000

    if xp < 500:
        level = xp / 500
    elif xp < 1500:
        level = 1 + (xp - 500) / 1000
    elif xp < 3500:
        level = 2 + (xp - 1500) / 2000
    elif xp < 7000:
        level = 3 + (xp - 3500) / 3500
    else:
        level = 4 + (xp - 7000) / 5000

    return prestiges * 100 + level
