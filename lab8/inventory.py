"""Модель складской позиции с валидируемыми свойствами."""

from __future__ import annotations


class InventoryItem:
    """Позиция склада с количеством, ценой и скидкой."""

    def __init__(
        self,
        name: str,
        quantity: int,
        unit_price: float,
    ) -> None:
        """Создаёт позицию с заданными названием и параметрами."""
        self.name = name
        self._quantity = 0
        self._unit_price = 0.0
        self.quantity = quantity
        self.unit_price = unit_price

    @property
    def quantity(self) -> int:
        """Текущее количество единиц, не меньше нуля."""
        return self._quantity

    @quantity.setter
    def quantity(self, value: int) -> None:
        """Принимает только целое неотрицательное количество."""
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(
                "quantity must be a non-negative integer"
            )
        if value < 0:
            raise ValueError(
                "quantity must be a non-negative integer"
            )
        self._quantity = value

    @property
    def unit_price(self) -> float:
        """Текущая цена единицы товара."""
        return round(self._unit_price, 2)

    @unit_price.setter
    def unit_price(self, value: float) -> None:
        """Принимает только положительную цену единицы."""
        if isinstance(value, bool) or not isinstance(
            value,
            (int, float),
        ):
            raise ValueError("unit_price must be a positive number")
        if value <= 0:
            raise ValueError("unit_price must be a positive number")
        self._unit_price = float(value)

    @property
    def total_value(self) -> float:
        """Стоимость позиции: количество умножить на цену."""
        return round(self._quantity * self._unit_price, 2)

    def add(self, amount: int) -> None:
        """Увеличивает количество на указанное число единиц."""
        amount = self._validate_amount(amount)
        self.quantity = self.quantity + amount

    def remove(self, amount: int) -> None:
        """Уменьшает количество на указанное число единиц."""
        amount = self._validate_amount(amount)
        if amount > self.quantity:
            raise ValueError(
                "cannot remove more than available quantity"
            )
        self.quantity = self.quantity - amount

    def apply_discount(self, percent: float) -> None:
        """Применяет скидку в процентах от 0 до 100."""
        if isinstance(percent, bool) or not isinstance(
            percent,
            (int, float),
        ):
            raise ValueError(
                "discount percent must be between 0 and 100"
            )
        if not 0 <= percent <= 100:
            raise ValueError(
                "discount percent must be between 0 and 100"
            )
        self._unit_price = round(
            self._unit_price * (1 - percent / 100),
            2,
        )

    @staticmethod
    def _validate_amount(amount: int) -> int:
        """Проверяет, что изменение количества корректно."""
        if isinstance(amount, bool) or not isinstance(amount, int):
            raise ValueError(
                "amount must be a non-negative integer"
            )
        if amount < 0:
            raise ValueError(
                "amount must be a non-negative integer"
            )
        return amount
