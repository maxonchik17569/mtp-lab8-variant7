# Отчёт по лабораторной работе №8

Ким Максим Сергеевич, группа 221341, вариант 7.

Тема: экосистема Python — Poetry, pytest, TDD, asyncio, FastAPI.

## Средняя сложность

### №7 — использовать logging

Модуль `lab8/logging_setup.py`:

- `configure_logging(level=logging.INFO) -> logging.Logger` возвращает
  общий логгер `lab8`, выставляет ему уровень и создаёт один
  `StreamHandler` с форматом
  `%(asctime)s | %(levelname)s | %(name)s | %(message)s`
  (время, уровень, имя логгера, сообщение).
- Обработчик хранится в модульной переменной и переиспользуется:
  повторный вызов меняет уровень логгера и обработчика, но не
  добавляет второй `StreamHandler`.
- `log_operation(logger, operation, **fields)` пишет операцию на
  уровне `INFO` в виде `operation=<имя> fields={...}` и дополнительно
  кладёт `operation` и `fields` в `LogRecord` через `extra`, поэтому
  тесты могут проверять структурированные поля, а не только текст.

Тесты `tests/test_logging_setup.py` проверяют имя и уровень логгера,
формат через реальный `LogRecord`, отсутствие дублирования
обработчиков при трёх последовательных вызовах, перехват записи
кастомным `_CollectingHandler` и через `caplog`.

### №9 — класс с property

Модуль `lab8/inventory.py`, класс `InventoryItem`:

- `quantity` — property с сеттером: принимается только целое
  неотрицательное число; `bool`, `float` и строки отклоняются
  `ValueError`.
- `unit_price` — property с сеттером: принимается только
  положительное число.
- `total_value` — вычисляемое property: `quantity * unit_price`,
  округление до двух знаков.
- `add(amount)` и `remove(amount)` валидируют целое неотрицательное
  изменение; `remove` больше остатка бросает `ValueError`.
- `apply_discount(percent)` принимает число от 0 до 100 включительно
  и уменьшает цену единицы. Скидка 100 % обнуляет стоимость позиции;
  явная установка нулевой или отрицательной цены через сеттер при
  этом по-прежнему запрещена.

Тесты `tests/test_inventory.py` покрывают нулевое количество,
положительные значения, все границы (`0`, `100`), неверные типы,
превышение остатка при списании и изменение стоимости после скидки.

### №3 — простая функция и тест pytest

Модуль `lab8/textstats.py`:

- `word_count(text) -> int` считает слова регулярным выражением
  `[^\W_]+(?:['-][^\W_]+)*`; поддерживаются кириллица, дефисы и
  апострофы внутри слова, знаки препинания словами не считаются.
- `top_words(text, limit=5)` возвращает список `(слово, частота)` в
  нижнем регистре; при равной частоте слова сортируются по алфавиту,
  поэтому результат детерминирован. Отрицательный `limit` — ошибка.

Тесты `tests/test_textstats.py` проверяют пустую строку, пунктуацию,
кириллицу, дефис и апостроф, частотный порядок, лимит и регистр.

## Повышенная сложность

### №7 — asyncio для многозадачности

Модуль `lab8/async_jobs.py`:

- `run_jobs(items, fetcher, limit=3)` создаёт `asyncio.Semaphore(limit)`
  и запускает по одной корутине на элемент через `asyncio.gather`.
- Семафор ограничивает число одновременно работающих `fetcher`;
  `gather` сохраняет порядок результатов независимо от порядка
  завершения задач.
- Исключение любой задачи не подавляется, а пробрасывается
  вызывающему коду; неположительный `limit` проверяется до запуска.

Тесты `tests/test_async_jobs.py` используют фейковый асинхронный
`fetcher` с `asyncio.sleep(0)`, считают `max_active` и проверяют
лимиты 1, 2 и 3, сохранение порядка при разном времени завершения,
проброс `RuntimeError`, пустой список и недопустимый лимит.

### №5 — TDD для API

Модуль `lab8/quotes_api.py` — REST API цитат на FastAPI:

- Pydantic-модели `QuoteCreate` (`text`, `author` с ограничениями
  длины) и `Quote` (добавляет `id`).
- `GET /quotes` — список цитат в порядке добавления.
- `GET /quotes/random` — случайная цитата; для пустого хранилища 404.
- `POST /quotes` — создание цитаты, ответ 201 с присвоенным `id`.
- `DELETE /quotes/{quote_id}` — 204 при успехе и 404 для
  отсутствующего идентификатора.
- Хранилище in-memory (`dict` + счётчик); `reset_quotes()` очищает
  словарь и сбрасывает счётчик, поэтому тесты изолированы.

Тесты `tests/test_quotes_api.py` используют `TestClient` (httpx) и
проверяют пустой список, создание и последовательные `id`, список,
случайную цитату, удаление с телом `b""`, 404 и валидацию Pydantic
(422).

## TDD-цикл

TDD применялся ко всем пяти заданиям: сначала были созданы пять
файлов тестов, затем запущен pytest. На этом состоянии модулей ещё
не было, и сбор тестов завершилась красным результатом:

```text
ERROR tests/test_async_jobs.py
ERROR tests/test_inventory.py
ERROR tests/test_logging_setup.py
ERROR tests/test_quotes_api.py
ERROR tests/test_textstats.py
!!!!!!!!!!!!!!!!!!! Interrupted: 5 errors during collection !!!!!!!!!!!!!!!!!!!!
1 warning, 5 errors in 0.63s
```

Причина каждого падения — отсутствие целевого модуля, например:

```text
tests/test_logging_setup.py:8: in <module>
    from lab8.logging_setup import configure_logging, log_operation
E   ModuleNotFoundError: No module named 'lab8.logging_setup'
```

После этого были написаны минимальные реализации пяти модулей и
точка входа `lab8/__main__.py`. Повторный прогон дал зелёный
результат:

```text
55 passed in 0.27s
```

Распределение тестов:

| Файл | Тестов |
| --- | ---: |
| `tests/test_logging_setup.py` | 5 |
| `tests/test_inventory.py` | 21 |
| `tests/test_textstats.py` | 9 |
| `tests/test_async_jobs.py` | 9 |
| `tests/test_quotes_api.py` | 11 |
| **Всего** | **55** |

Для API цикл red → green был содержательным: тесты фиксировали
статусы 201/204/404/422 и формат JSON до появления маршрутов, затем
реализация подгонялась под тесты, а не наоборот. После зелёного
прогона код проверен flake8; подавлять ошибки и менять тесты под
реализацию не потребовалось.

## Экосистема Poetry и pytest

- `pyproject.toml` оформлен в формате Poetry: `[tool.poetry]` с
  именем `mtp-lab8-variant7`, версией `1.0.0`, автором и пакетом
  `lab8`; зависимости `python = "^3.11"`, `fastapi`, `uvicorn`;
  dev-группа — `pytest`, `httpx`, `flake8`; build-system —
  `poetry-core`.
- `[tool.pytest.ini_options]` задаёт `testpaths = ["tests"]`.
  Дополнительно указан `pythonpath = ["."]`, потому что в
  обязательной структуре нет `tests/__init__.py`: без этого
  pytest не находил бы пакет `lab8` при импорте из тестов.
- `setup.cfg` — отдельный конфиг flake8 с `max-line-length = 79`:
  flake8 не читает настройки из `pyproject.toml`.
- `requirements-dev.txt` повторяет dev-зависимости для CI без Poetry.
- Workflow `.github/workflows/python-checks.yml` ставит Python 3.13,
  зависимости из `requirements-dev.txt`, запускает flake8,
  `compileall` и `pytest -q`.

## Проверки

Полный прогон тестов:

```text
$ uv run --with pytest --with fastapi --with httpx pytest -q
55 passed in 0.27s
```

Стиль кода (flake8 молчит, поэтому показан код возврата):

```text
$ uv run --with flake8 flake8 lab8 tests
flake8 exit: 0
```

Компиляция байткода:

```text
$ uv run python -m compileall -q lab8 tests
compileall exit: 0
```

Демонстрация без uvicorn и без сети:

```text
$ uv run --with fastapi --with httpx python -m lab8
word_count: 6
top_words: [('python', 2), ('asyncio', 1), ('fastapi', 1)]
async lengths: [3, 3, 5]
create quote: 201 {'text': 'Тесты — это документация.', 'author': 'Ким', 'id': 1}
list quotes: [{'text': 'Тесты — это документация.', 'author': 'Ким', 'id': 1}]
random quote: {'text': 'Тесты — это документация.', 'author': 'Ким', 'id': 1}
demo exit: 0
```

Примечание: установленная версия Starlette предупреждает об
устаревании связки `TestClient` с `httpx` и предлагает `httpx2`.
Требование варианта фиксирует `httpx`, поэтому предупреждение
отфильтровано только на уровне pytest; на работу API и тестов оно
не влияет.
