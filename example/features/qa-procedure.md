# QA procedure: checkout totals

*Written by the specifier seat, from a human's point of view. The QA seat turns it into an executable script; a person can also follow it by hand.*

**You are a person using this shop. Prove that checkout works.**

The example shop has no web UI, so its "user interface" is the Python API. Open a shell at the repository root:

```bash
python -i -c "import sys; sys.path.insert(0, 'example')"
```

```python
>>> from shop.cart import Cart
>>> from shop.storage import InMemoryCartStore
>>> from shop.checkout import checkout
>>> store = InMemoryCartStore()
```

| # | Action | Expected result |
|---|---|---|
| 1 | Make a cart with one $20.00 book: `c = Cart(); c.add("book", 2000); store.save("a", c)` | No error |
| 2 | `checkout("a", store)` | `Receipt(subtotal_cents=2000, discount_cents=0, shipping_cents=499, total_cents=2499)` |
| 3 | Make a cart with exactly ten $10.00 widgets: `c = Cart(); c.add("w", 1000, 10); store.save("b", c)` | No error |
| 4 | `checkout("b", store)` | Discount is exactly `1000`, shipping is `0`, total `9000` |
| 5 | `checkout("b", store, coupon="WELCOME5")` | Discount `1500`, total `8500` |
| 6 | `checkout("b", store, coupon="FREEMONEY")` | Raises `ValueError` mentioning the unknown coupon |
| 7 | `checkout("missing", store)` | Raises `KeyError`, so a missing cart fails loudly rather than producing an empty receipt |
| 8 | Try to change a receipt: `r = checkout("a", store); r.total_cents = 0` | Raises `FrozenInstanceError`; receipts can't be altered |

**Pass** = every row behaves as expected. Record any mismatch with the step number and what you saw.
