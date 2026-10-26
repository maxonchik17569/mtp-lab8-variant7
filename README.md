# Лабораторная работа №8

Ким Максим Сергеевич, группа 221341, вариант 7, лабораторная №8.

Тема: экосистема Python — Poetry, pytest, TDD, asyncio, FastAPI.

## Задания варианта

**Средняя сложность:**

- №7 — использовать logging (`lab8/logging_setup.py`,
  `tests/test_logging_setup.py`)
- №9 — создать класс с property (`lab8/inventory.py`,
  `tests/test_inventory.py`)
- №3 — написать простую функцию и тест pytest (`lab8/textstats.py`,
  `tests/test_textstats.py`)

**Повышенная сложность:**

- №7 — использовать asyncio для многозадачности
  (`lab8/async_jobs.py`, `tests/test_async_jobs.py`)
- №5 — применить TDD к API (`lab8/quotes_api.py`,
  `tests/test_quotes_api.py`)

## Клонирование

```bash
git clone https://github.com/maxonchik17569/mtp-lab8-variant7.git
cd mtp-lab8-variant7
```

## Запуск

Демонстрация всех заданий без запуска uvicorn и без сетевых
запросов:

```bash
uv run --with fastapi --with httpx python -m lab8
```

Демонстрация настраивает logging, создаёт `InventoryItem`,
считает слова, запускает asyncio-задачи и выполняет запросы к
FastAPI через `TestClient`.

## Тесты

```bash
uv run --with pytest --with fastapi --with httpx pytest -q
```

## Проверки

```bash
uv run --with flake8 flake8 lab8 tests
uv run python -m compileall -q lab8 tests
```

Зависимости описаны в `pyproject.toml` (формат Poetry).
`requirements-dev.txt` используется в CI без Poetry, `setup.cfg`
задаёт `max-line-length = 79` для flake8. Workflow
`.github/workflows/python-checks.yml` запускает flake8,
`compileall` и pytest на Python 3.13.

Подробный отчёт по заданиям и TDD-циклу — в `docs/report.md`.

## Требования

- Python 3.13 или новее.
- [uv](https://docs.astral.sh/uv/) для запуска без ручной установки
  зависимостей.
- `pytest`, `fastapi`, `httpx` и `flake8` ставятся командами `uv run`.
- Poetry-конфигурация лежит в `pyproject.toml`; для проверок достаточно
  `requirements-dev.txt`.
