"""Where carts live between requests. Depends only on the cart."""

from shop.cart import Cart


class InMemoryCartStore:
    def __init__(self) -> None:
        self._carts: dict[str, Cart] = {}

    def save(self, cart_id: str, cart: Cart) -> None:
        self._carts[cart_id] = cart

    def load(self, cart_id: str) -> Cart:
        if cart_id not in self._carts:
            raise KeyError(f"no cart with id {cart_id!r}")
        return self._carts[cart_id]
