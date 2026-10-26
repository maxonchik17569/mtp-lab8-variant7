"""Тесты REST API цитат, написанные до реализации (TDD)."""

import pytest
from fastapi.testclient import TestClient

from lab8.quotes_api import app, reset_quotes

client = TestClient(app)


@pytest.fixture(autouse=True)
def _clean_store() -> None:
    """Сбрасывает хранилище перед каждым тестом."""
    reset_quotes()


def _create_quote(
    text: str = "Текст",
    author: str = "Автор",
) -> dict[str, object]:
    """Создаёт цитату и проверяет код ответа."""
    response = client.post(
        "/quotes",
        json={"text": text, "author": author},
    )
    assert response.status_code == 201
    return response.json()


def test_list_quotes_returns_empty_list() -> None:
    """Новое хранилище не содержит цитат."""
    response = client.get("/quotes")
    assert response.status_code == 200
    assert response.json() == []


def test_create_quote_returns_201_and_payload() -> None:
    """POST создаёт цитату и возвращает её с идентификатором."""
    response = client.post(
        "/quotes",
        json={"text": "Простота лучше сложности.", "author": "Ким"},
    )
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "text": "Простота лучше сложности.",
        "author": "Ким",
    }


def test_create_quote_increments_identifier() -> None:
    """Идентификаторы выдаются последовательно."""
    first = _create_quote("Первая", "A")
    second = _create_quote("Вторая", "B")
    assert (first["id"], second["id"]) == (1, 2)


def test_list_quotes_returns_created_quotes() -> None:
    """GET /quotes возвращает цитаты в порядке добавления."""
    _create_quote("Первая", "A")
    _create_quote("Вторая", "B")
    response = client.get("/quotes")
    assert [item["text"] for item in response.json()] == [
        "Первая",
        "Вторая",
    ]


def test_random_quote_returns_existing_quote() -> None:
    """При одной цитате случайный выбор однозначен."""
    created = _create_quote("Единственная", "A")
    response = client.get("/quotes/random")
    assert response.status_code == 200
    assert response.json() == created


def test_random_quote_returns_404_for_empty_store() -> None:
    """Для пустого хранилища случайная цитата не существует."""
    response = client.get("/quotes/random")
    assert response.status_code == 404


def test_delete_quote_returns_204_and_removes_quote() -> None:
    """DELETE удаляет цитату и отвечает без тела."""
    created = _create_quote()
    response = client.delete(f"/quotes/{created['id']}")
    assert response.status_code == 204
    assert response.content == b""
    assert client.get("/quotes").json() == []


def test_delete_missing_quote_returns_404() -> None:
    """Удаление отсутствующей цитаты даёт 404."""
    response = client.delete("/quotes/999")
    assert response.status_code == 404


@pytest.mark.parametrize(
    "payload",
    [
        {"text": "", "author": "A"},
        {"text": "T", "author": ""},
        {},
    ],
)
def test_create_quote_validates_payload(
    payload: dict[str, str],
) -> None:
    """Пустые поля и отсутствие данных отклоняются Pydantic."""
    response = client.post("/quotes", json=payload)
    assert response.status_code == 422
