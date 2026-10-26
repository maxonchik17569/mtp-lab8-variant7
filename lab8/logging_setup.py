"""Настройка журналирования для модулей лабораторной работы."""

import logging

LOGGER_NAME = "lab8"
_LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
_stream_handler: logging.StreamHandler | None = None


def configure_logging(level: int = logging.INFO) -> logging.Logger:
    """Настраивает общий логгер lab8 и возвращает его.

    Повторный вызов обновляет уровень, но не добавляет второй
    потоковый обработчик.
    """
    global _stream_handler
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(level)
    if _stream_handler is None or _stream_handler not in logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(_LOG_FORMAT))
        _stream_handler = handler
        logger.addHandler(handler)
    _stream_handler.setLevel(level)
    return logger


def log_operation(
    logger: logging.Logger,
    operation: str,
    **fields: object,
) -> None:
    """Записывает операцию и её именованные поля на уровне INFO."""
    logger.info(
        "operation=%s fields=%s",
        operation,
        fields,
        extra={"operation": operation, "fields": fields},
    )
