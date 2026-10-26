"""Тесты настройки журналирования."""

import logging
import re

import pytest

from lab8.logging_setup import configure_logging, log_operation


class _CollectingHandler(logging.Handler):
    """Собирает записи журнала для проверок."""

    def __init__(self) -> None:
        super().__init__()
        self.records: list[logging.LogRecord] = []

    def emit(self, record: logging.LogRecord) -> None:
        """Сохраняет запись в список."""
        self.records.append(record)


@pytest.fixture(autouse=True)
def _default_log_level() -> None:
    """Возвращает общий логгер к уровню INFO перед каждым тестом."""
    configure_logging(logging.INFO)


def test_configure_logging_returns_lab8_logger() -> None:
    """Возвращает логгер lab8 с заданным уровнем."""
    logger = configure_logging(logging.DEBUG)
    assert logger.name == "lab8"
    assert logger.level == logging.DEBUG


def test_configure_logging_sets_stream_formatter() -> None:
    """Потоковый обработчик печатает время, уровень, имя и текст."""
    logger = configure_logging(logging.INFO)
    handlers = [
        handler
        for handler in logger.handlers
        if isinstance(handler, logging.StreamHandler)
    ]
    assert handlers
    formatter = handlers[0].formatter
    assert formatter is not None
    record = logging.LogRecord(
        "lab8",
        logging.INFO,
        __file__,
        1,
        "проверка",
        None,
        None,
    )
    output = formatter.format(record)
    assert re.search(r"\d{4}-\d{2}-\d{2}", output)
    assert "INFO" in output
    assert "lab8" in output
    assert "проверка" in output


def test_configure_logging_does_not_duplicate_handlers() -> None:
    """Повторный вызов обновляет уровень, но не плодит обработчики."""
    logger = configure_logging(logging.INFO)
    count = len(logger.handlers)
    configure_logging(logging.WARNING)
    assert len(logger.handlers) == count
    assert logger.level == logging.WARNING
    configure_logging(logging.DEBUG)
    assert len(logger.handlers) == count
    assert logger.level == logging.DEBUG


def test_log_operation_writes_fields_to_custom_handler() -> None:
    """Операция и её поля попадают в запись журнала."""
    logger = configure_logging(logging.INFO)
    handler = _CollectingHandler()
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)
    try:
        log_operation(logger, "add_item", sku="A-1", amount=2)
    finally:
        logger.removeHandler(handler)
    assert len(handler.records) == 1
    record = handler.records[0]
    assert record.getMessage().startswith("operation=add_item")
    assert getattr(record, "operation") == "add_item"
    assert getattr(record, "fields") == {"sku": "A-1", "amount": 2}


def test_log_operation_is_visible_through_caplog(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Запись операции перехватывается стандартным caplog."""
    logger = configure_logging(logging.INFO)
    caplog.set_level(logging.INFO, logger="lab8")
    log_operation(logger, "demo", value=1)
    messages = [record.getMessage() for record in caplog.records]
    assert any("operation=demo" in message for message in messages)
