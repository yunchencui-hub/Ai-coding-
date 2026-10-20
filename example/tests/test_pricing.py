import pytest

from shop.cart import Cart
from shop.pricing import bulk_discount_cents, coupon_discount_cents, shipping_cents


def cart_with(quantity: int, unit_price_cents: int = 1000) -> Cart:
    cart = Cart()
    cart.add("widget", unit_price_cents, quantity)
    return cart


def test_no_bulk_discount_below_ten_items():
    assert bulk_discount_cents(cart_with(9)) == 0


def test_bulk_discount_starts_at_exactly_ten_items():
    # 10 x $10.00 = $100.00, and 10% of that is $10.00
    assert bulk_discount_cents(cart_with(10)) == 1000


def test_bulk_discount_rounds_down_to_whole_cents():
    # 10 x 99c = 990c, and 10% is exactly 99c.
    assert bulk_discount_cents(cart_with(10, 99)) == 99
    # 11 x 95c = 1045c, and 10% is 104.5c, which rounds down to 104c.
    assert bulk_discount_cents(cart_with(11, 95)) == 104


def test_no_coupon_means_no_discount():
    assert coupon_discount_cents(None) == 0


def test_known_coupon_takes_five_dollars_off():
    assert coupon_discount_cents("WELCOME5") == 500


def test_unknown_coupon_is_rejected():
    with pytest.raises(ValueError):
        coupon_discount_cents("FREEMONEY")


def test_shipping_is_charged_just_below_the_threshold():
    assert shipping_cents(4999) == 499


def test_shipping_is_free_at_exactly_fifty_dollars():
    assert shipping_cents(5000) == 0
