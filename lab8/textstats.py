"""Простые статистические функции для текста."""

from __future__ import annotations

import re
from collections import Counter

_WORD_PATTERN = re.compile(r"[^\W_]+(?:['-][^\W_]+)*", re.UNICODE)


def word_count(text: str) -> int:
    """Возвращает число слов в тексте.

    Знаки препинания не считаются словами, а дефисы и апострофы
    внутри слова сохраняют его целостность.
    """
    return len(_WORD_PATTERN.findall(text))


def top_words(
    text: str,
    limit: int = 5,
) -> list[tuple[str, int]]:
    """Возвращает самые частые слова в нижнем регистре.

    При равной частоте слова сортируются по алфавиту, поэтому
    результат детерминирован.
    """
    if limit < 0:
        raise ValueError("limit must be non-negative")
    counts = Counter(
        match.group(0).lower()
        for match in _WORD_PATTERN.finditer(text)
    )
    ordered = sorted(
        counts.items(),
        key=lambda item: (-item[1], item[0]),
    )
    return ordered[:limit]
