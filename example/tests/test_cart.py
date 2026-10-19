import dataclasses

import pytest

from shop.cart import Cart, LineItem


def test_line_item_is_immutable():
    # Added after tools/mutate.py reported `frozen=True -> False` survived:
    # no test noticed if line items could be edited after being added.
    with pytest.raises(dataclasses.FrozenInstanceError):
        LineItem("apple", 250).quantity = 99


def test_line_item_defaults_to_one_unit():
    assert LineItem("apple", 250).quantity == 1


def test_line_item_total_is_price_times_quantity():
    assert LineItem("apple", 250, 3).total_cents == 750


def test_add_defaults_to_one_unit():
    cart = Cart()
    cart.add("apple", 250)
    assert cart.item_count() == 1


def test_add_accepts_a_single_unit():
    cart = Cart()
    cart.add("apple", 250, quantity=1)
    assert cart.subtotal_cents() == 250


def test_add_rejects_zero_quantity():
    with pytest.raises(ValueError):
        Cart().add("apple", 250, quantity=0)


def test_subtotal_and_count_sum_across_items():
    cart = Cart()
    cart.add("apple", 250, quantity=2)
    cart.add("pear", 100, quantity=3)
    assert cart.subtotal_cents() == 800
    assert cart.item_count() == 5
