"""Runs the Examples table in example/features/checkout.feature as tests.

This is the coder seat's job in miniature: make the specifier's Gherkin pass.
A real project would use a Gherkin runner (pytest-bdd, behave, Cucumber);
this small parser keeps the example dependency-free.
"""

from pathlib import Path

import pytest

from shop.cart import Cart
from shop.checkout import Receipt, checkout
from shop.storage import InMemoryCartStore

FEATURE = Path(__file__).resolve().parent.parent / "features" / "checkout.feature"


def example_rows() -> list[dict[str, str]]:
    lines = [line.strip() for line in FEATURE.read_text().splitlines()]
    table = [line for line in lines[lines.index("Examples:") + 1:] if line.startswith("|")]
    header, *rows = [[cell.strip() for cell in line.strip("|").split("|")] for line in table]
    return [dict(zip(header, row)) for row in rows]


def test_the_feature_file_has_examples():
    assert len(example_rows()) >= 8


@pytest.mark.parametrize("row", example_rows(),
                         ids=lambda r: f"{r['quantity']}x{r['unit price']}-{r['coupon']}")
def test_checkout_matches_the_feature_file(row):
    cart = Cart()
    cart.add("item", int(row["unit price"]), int(row["quantity"]))
    store = InMemoryCartStore()
    store.save("cart", cart)
    coupon = None if row["coupon"] == "none" else row["coupon"]

    receipt = checkout("cart", store, coupon)

    assert receipt == Receipt(int(row["subtotal"]), int(row["discount"]),
                              int(row["shipping"]), int(row["total"]))
