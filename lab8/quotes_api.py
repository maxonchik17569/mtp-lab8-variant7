"""REST API цитат на FastAPI, разработанный по TDD."""

from __future__ import annotations

import random
from typing import Final

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Lab 8 Quotes API", version="1.0.0")

_quotes: dict[int, "Quote"] = {}
_next_id: int = 1
_MAX_TEXT_LENGTH: Final[int] = 500
_MAX_AUTHOR_LENGTH: Final[int] = 100


class QuoteCreate(BaseModel):
    """Данные для создания новой цитаты."""

    text: str = Field(min_length=1, max_length=_MAX_TEXT_LENGTH)
    author: str = Field(min_length=1, max_length=_MAX_AUTHOR_LENGTH)


class Quote(QuoteCreate):
    """Цитата с присвоенным идентификатором."""

    id: int


def reset_quotes() -> None:
    """Очищает хранилище и сбрасывает счётчик идентификаторов."""
    global _next_id
    _quotes.clear()
    _next_id = 1


@app.get("/quotes", response_model=list[Quote])
def list_quotes() -> list[Quote]:
    """Возвращает все цитаты в порядке добавления."""
    return list(_quotes.values())


@app.get("/quotes/random", response_model=Quote)
def random_quote() -> Quote:
    """Возвращает случайную цитату или 404 для пустого хранилища."""
    if not _quotes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no quotes available",
        )
    return random.choice(list(_quotes.values()))


@app.post(
    "/quotes",
    response_model=Quote,
    status_code=status.HTTP_201_CREATED,
)
def create_quote(payload: QuoteCreate) -> Quote:
    """Создаёт цитату и присваивает ей следующий идентификатор."""
    global _next_id
    quote = Quote(id=_next_id, **payload.model_dump())
    _quotes[quote.id] = quote
    _next_id += 1
    return quote


@app.delete(
    "/quotes/{quote_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_quote(quote_id: int) -> None:
    """Удаляет цитату; для отсутствующего id возвращает 404."""
    if quote_id not in _quotes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="quote not found",
        )
    del _quotes[quote_id]
