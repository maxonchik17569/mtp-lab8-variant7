"""Демонстрация всех заданий лабораторной работы №8."""

from __future__ import annotations

import asyncio

from fastapi.testclient import TestClient

from lab8.async_jobs import run_jobs
from lab8.inventory import InventoryItem
from lab8.logging_setup import configure_logging, log_operation
from lab8.quotes_api import app, reset_quotes
from lab8.textstats import top_words, word_count


async def _fetch_length(text: str) -> int:
    """Имитирует асинхронное получение длины строки."""
    await asyncio.sleep(0)
    return len(text)


def main() -> int:
    """Запускает демонстрацию без сети и без uvicorn."""
    logger = configure_logging()
    logger.info("демонстрация лабораторной работы №8")

    item = InventoryItem("Кабель USB-C", 10, 250.0)
    item.add(5)
    item.remove(3)
    item.apply_discount(10)
    log_operation(
        logger,
        "inventory_check",
        quantity=item.quantity,
        total=item.total_value,
    )

    text = "Python pytest TDD asyncio FastAPI Python"
    print(f"word_count: {word_count(text)}")
    print(f"top_words: {top_words(text, limit=3)}")

    lengths = asyncio.run(
        run_jobs(["one", "two", "three"], _fetch_length, limit=2)
    )
    print(f"async lengths: {lengths}")

    reset_quotes()
    client = TestClient(app)
    created = client.post(
        "/quotes",
        json={"text": "Тесты — это документация.", "author": "Ким"},
    )
    print(f"create quote: {created.status_code} {created.json()}")
    print(f"list quotes: {client.get('/quotes').json()}")
    print(f"random quote: {client.get('/quotes/random').json()}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
