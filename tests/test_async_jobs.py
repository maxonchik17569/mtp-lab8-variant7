"""Тесты асинхронного запуска задач с ограничением."""

import asyncio

import pytest

from lab8.async_jobs import run_jobs


def test_run_jobs_preserves_input_order() -> None:
    """Результаты идут в порядке входных элементов."""

    async def fetcher(value: int) -> int:
        await asyncio.sleep(0.01 if value == 1 else 0)
        return value * 10

    result = asyncio.run(run_jobs([1, 2, 3], fetcher))
    assert result == [10, 20, 30]


@pytest.mark.parametrize(("limit", "expected"), [(1, 1), (2, 2), (3, 3)])
def test_run_jobs_respects_concurrency_limit(
    limit: int,
    expected: int,
) -> None:
    """Число одновременных задач не превышает limit."""
    active = 0
    max_active = 0

    async def fetcher(value: int) -> int:
        nonlocal active, max_active
        active += 1
        max_active = max(max_active, active)
        await asyncio.sleep(0)
        active -= 1
        return value

    result = asyncio.run(run_jobs(list(range(1, 6)), fetcher, limit=limit))

    assert result == [1, 2, 3, 4, 5]
    assert max_active == expected


def test_run_jobs_propagates_fetcher_error() -> None:
    """Исключение задачи пробрасывается наружу."""

    async def fetcher(value: int) -> int:
        await asyncio.sleep(0)
        if value == 2:
            raise RuntimeError("boom")
        return value

    with pytest.raises(RuntimeError, match="boom"):
        asyncio.run(run_jobs([1, 2, 3], fetcher))


def test_run_jobs_returns_empty_list_for_no_items() -> None:
    """Пустой список элементов даёт пустой результат."""

    async def fetcher(value: int) -> int:
        return value

    assert asyncio.run(run_jobs([], fetcher)) == []


@pytest.mark.parametrize("limit", [0, -1, True])
def test_run_jobs_rejects_non_positive_limit(limit: object) -> None:
    """Лимит должен быть положительным целым числом."""

    async def fetcher(value: int) -> int:
        return value

    with pytest.raises(ValueError):
        asyncio.run(
            run_jobs([1], fetcher, limit=limit)  # type: ignore[arg-type]
        )
