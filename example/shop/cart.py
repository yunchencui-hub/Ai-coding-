"""What the customer wants to buy. Depends on nothing else in the shop."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class LineItem:
    sku: str
    unit_price_cents: int
    quantity: int = 1

    @property
    def total_cents(self) -> int:
        return self.unit_price_cents * self.quantity


@dataclass
class Cart:
    items: list[LineItem] = field(default_factory=list)

    def add(self, sku: str, unit_price_cents: int, quantity: int = 1) -> None:
        if quantity < 1:
            raise ValueError("quantity must be at least 1")
        self.items.append(LineItem(sku, unit_price_cents, quantity))

    def subtotal_cents(self) -> int:
        return sum(item.total_cents for item in self.items)

    def item_count(self) -> int:
        return sum(item.quantity for item in self.items)
