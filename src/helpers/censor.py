import re

BAD_WORDS = [
    # Profanity
    "fuck", "fucking", "fucker", "motherfucker",
    "shit", "shitty",
    "bitch", "bitches",
    "ass", "asshole", "asshat",
    "bastard",
    "damn", "goddamn",
    "crap",
    "piss",
    "dick", "dickhead",
    "cock",
    "prick",
    "twat",
    "wanker",

    # Insults
    "idiot",
    "moron",
    "retard",
    "dumbass",
    "jackass",
    "loser",
    "dipshit",
    "scumbag",

    # Sexual
    "whore",
    "slut",
    "cunt",

    # Drugs
    "weed",
    "marijuana",
    "cannabis",
    "cocaine",
    "crack",
    "heroin",
    "meth",
    "methamphetamine",
    "lsd",
    "ecstasy",
    "mdma",
    "ketamine",
    "fentanyl",
    "opioid",
    "opium",
    "mushrooms",
    "shrooms",

    # Violence
    "murder",
    "kill",
    "killing",
    "suicide",
    "bomb",
    "explosive",
    "terrorist",

    # Weapons
    "gun",
    "rifle",
    "pistol",
    "shotgun",
    "sniper",
    "grenade",
    "knife",

    # Common bypasses
    "fck",
    "fk",
    "fuk",
    "sh1t",
    "b1tch",
]


def _make_pattern(word: str) -> str:
    return r"[\W_]*".join(map(re.escape, word))


pattern = re.compile(
    r"\b(?:"
    + "|".join(_make_pattern(word) for word in BAD_WORDS)
    + r")\b",
    re.IGNORECASE,
)


def censor(text: str) -> str:
    return pattern.sub(lambda m: "*" * len(m.group()), text)
