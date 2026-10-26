"""Тесты простых функций статистики текста."""

import pytest

from lab8.textstats import top_words, word_count


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("", 0),
        ("Hello, world!", 2),
        ("Привет, мир!", 2),
        ("well-known don't stop", 3),
        ("  ...  ", 0),
    ],
)
def test_word_count(text: str, expected: int) -> None:
    """Функция считает слова и игнорирует знаки препинания."""
    assert word_count(text) == expected


def test_top_words_returns_frequency_order() -> None:
    """Слова сортируются по частоте, затем по алфавиту."""
    text = "b a b c a b"
    assert top_words(text) == [("b", 3), ("a", 2), ("c", 1)]


def test_top_words_respects_limit() -> None:
    """Параметр limit ограничивает длину результата."""
    text = "b a b c a b"
    assert top_words(text, limit=2) == [("b", 3), ("a", 2)]
    assert top_words(text, limit=0) == []


def test_top_words_is_case_insensitive() -> None:
    """Слова приводятся к нижнему регистру перед подсчётом."""
    result = top_words("Python python PYTHON pytest")
    assert result[0] == ("python", 3)


def test_top_words_rejects_negative_limit() -> None:
    """Отрицательный limit не имеет смысла."""
    with pytest.raises(ValueError):
        top_words("a b", limit=-1)
