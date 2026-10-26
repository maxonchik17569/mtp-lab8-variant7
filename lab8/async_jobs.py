"""Параллельный запуск асинхронных задач с ограничением."""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable, Sequence
from typing import TypeVar

T = TypeVar("T")
R = TypeVar("R")


async def run_jobs(
    items: Sequence[T],
    fetcher: Callable[[T], Awaitable[R]],
    limit: int = 3,
) -> list[R]:
    """Запускает fetcher для элементов с лимитом одновременно.

    Результаты возвращаются в порядке items. Исключение любой
    задачи пробрасывается вызывающему коду.
    """
    if (
        isinstance(limit, bool)
        or not isinstance(limit, int)
        or limit < 1
    ):
        raise ValueError("limit must be a positive integer")
    semaphore = asyncio.Semaphore(limit)

    async def run_one(item: T) -> R:
        async with semaphore:
            return await fetcher(item)

    results = await asyncio.gather(
        *(run_one(item) for item in items)
    )
    return list(results)
