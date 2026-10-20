"""Turns a stored cart into a receipt.

Checkout needs to load carts, but it does not import shop.storage. It declares
the small interface it needs (CartStore) and lets the caller pass in any
object that fits. That is "insert an interface": the dependency now points
from storage toward the abstraction instead of from checkout toward storage.
"""

from dataclasses import dataclass
from typing import Protocol

from shop.cart import Cart
from shop.pricing import bulk_discount_cents, coupon_discount_cents, shipping_cents


class CartStore(Protocol):
    def load(self, cart_id: str) -> Cart: ...


@dataclass(frozen=True)
class Receipt:
    subtotal_cents: int
    discount_cents: int
    shipping_cents: int
    total_cents: int


def checkout(cart_id: str, store: CartStore, coupon: str | None = None) -> Receipt:
    cart = store.load(cart_id)
    subtotal = cart.subtotal_cents()
    discount = min(subtotal, bulk_discount_cents(cart) + coupon_discount_cents(coupon))
    shipping = shipping_cents(subtotal - discount)
    return Receipt(subtotal, discount, shipping, subtotal - discount + shipping)
