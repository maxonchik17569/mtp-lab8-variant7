"""Тесты модели складской позиции."""

import pytest

from lab8.inventory import InventoryItem


def test_total_value_multiplies_quantity_and_price() -> None:
    """Стоимость равна количеству, умноженному на цену."""
    item = InventoryItem("Кабель", 3, 12.5)
    assert item.total_value == 37.5


def test_quantity_accepts_zero() -> None:
    """Нулевое количество допустимо."""
    item = InventoryItem("Кабель", 0, 10.0)
    assert item.quantity == 0
    assert item.total_value == 0.0


@pytest.mark.parametrize("value", [-1, 1.5, True, "2"])
def test_quantity_rejects_invalid_values(value: object) -> None:
    """Количество должно быть целым и неотрицательным."""
    with pytest.raises(ValueError):
        InventoryItem("Кабель", value, 10.0)  # type: ignore[arg-type]


@pytest.mark.parametrize("value", [0, -1, True, "10"])
def test_unit_price_rejects_non_positive_values(value: object) -> None:
    """Цена должна быть положительным числом."""
    with pytest.raises(ValueError):
        InventoryItem("Кабель", 1, value)  # type: ignore[arg-type]


def test_setters_validate_new_values() -> None:
    """Свойства проверяют значения и после создания объекта."""
    item = InventoryItem("Кабель", 2, 10.0)
    item.quantity = 7
    item.unit_price = 5.5
    assert item.quantity == 7
    assert item.unit_price == 5.5
    with pytest.raises(ValueError):
        item.quantity = -1
    with pytest.raises(ValueError):
        item.unit_price = 0


def test_add_and_remove_update_quantity() -> None:
    """Методы add и remove меняют количество и стоимость."""
    item = InventoryItem("Кабель", 5, 10.0)
    item.add(3)
    assert item.quantity == 8
    assert item.total_value == 80.0
    item.remove(8)
    assert item.quantity == 0
    assert item.total_value == 0.0


@pytest.mark.parametrize("amount", [-1, 1.5, True])
def test_add_rejects_invalid_amounts(amount: object) -> None:
    """Добавлять можно только целое неотрицательное количество."""
    item = InventoryItem("Кабель", 5, 10.0)
    with pytest.raises(ValueError):
        item.add(amount)  # type: ignore[arg-type]


def test_remove_rejects_more_than_available() -> None:
    """Нельзя списать больше, чем есть на складе."""
    item = InventoryItem("Кабель", 2, 10.0)
    with pytest.raises(ValueError):
        item.remove(3)
    assert item.quantity == 2


def test_apply_discount_changes_price_and_total() -> None:
    """Скидка уменьшает цену единицы и общую стоимость."""
    item = InventoryItem("Кабель", 10, 100.0)
    item.apply_discount(25)
    assert item.unit_price == 75.0
    assert item.total_value == 750.0
    item.apply_discount(0)
    assert item.unit_price == 75.0
    item.apply_discount(100)
    assert item.total_value == 0.0


@pytest.mark.parametrize("percent", [-1, 101, "10", True])
def test_apply_discount_rejects_invalid_percent(percent: object) -> None:
    """Скидка задаётся числом от 0 до 100."""
    item = InventoryItem("Кабель", 1, 10.0)
    with pytest.raises(ValueError):
        item.apply_discount(percent)  # type: ignore[arg-type]
