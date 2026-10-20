import pytest

from shop.cart import Cart
from shop.storage import InMemoryCartStore


def test_saved_cart_can_be_loaded():
    store = InMemoryCartStore()
    cart = Cart()
    store.save("c1", cart)
    assert store.load("c1") is cart


def test_loading_a_missing_cart_fails_loudly():
    with pytest.raises(KeyError):
        InMemoryCartStore().load("nope")
