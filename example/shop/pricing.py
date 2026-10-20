"""Discount and shipping rules. Depends only on the cart."""

from shop.cart import Cart

BULK_THRESHOLD_ITEMS = 10
BULK_DISCOUNT_PERCENT = 10
COUPONS_CENTS_OFF = {"WELCOME5": 500}
FREE_SHIPPING_FROM_CENTS = 5000
SHIPPING_CENTS = 499


def bulk_discount_cents(cart: Cart) -> int:
    if cart.item_count() >= BULK_THRESHOLD_ITEMS:
        return cart.subtotal_cents() * BULK_DISCOUNT_PERCENT // 100
    return 0


def coupon_discount_cents(code: str | None) -> int:
    if code is None:
        return 0
    if code not in COUPONS_CENTS_OFF:
        raise ValueError(f"unknown coupon: {code}")
    return COUPONS_CENTS_OFF[code]


def shipping_cents(subtotal_after_discount_cents: int) -> int:
    if subtotal_after_discount_cents >= FREE_SHIPPING_FROM_CENTS:
        return 0
    return SHIPPING_CENTS
