import dataclasses

import pytest

from shop.cart import Cart
from shop.checkout import Receipt, checkout
from shop.storage import InMemoryCartStore


def test_receipts_cannot_be_altered():
    with pytest.raises(dataclasses.FrozenInstanceError):
        Receipt(100, 0, 499, 599).total_cents = 0


def stored(cart: Cart) -> InMemoryCartStore:
    store = InMemoryCartStore()
    store.save("c1", cart)
    return store


def test_small_order_pays_shipping():
    cart = Cart()
    cart.add("book", 2000)
    assert checkout("c1", stored(cart)) == Receipt(2000, 0, 499, 2499)


def test_coupon_can_push_an_order_back_under_free_shipping():
    # $52.00 qualifies for free shipping, but $52.00 - $5.00 = $47.00 does not.
    cart = Cart()
    cart.add("lamp", 5200)
    assert checkout("c1", stored(cart), coupon="WELCOME5") == Receipt(5200, 500, 499, 5199)


def test_bulk_and_coupon_discounts_add_up():
    cart = Cart()
    cart.add("widget", 1000, quantity=10)  # $100.00, bulk discount $10.00
    receipt = checkout("c1", stored(cart), coupon="WELCOME5")
    assert receipt == Receipt(10000, 1500, 0, 8500)


def test_discount_never_exceeds_the_subtotal():
    cart = Cart()
    cart.add("sticker", 300)
    assert checkout("c1", stored(cart), coupon="WELCOME5") == Receipt(300, 300, 499, 499)
