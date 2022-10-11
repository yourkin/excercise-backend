import random
import time

from app.types import Order


class OrderPlacementError(Exception):
    pass


def place_order(order: Order):
    """dummy function that is symbolicly standing for placing an order at the stock exchange"""

    if not order:
        raise ValueError("Required order parameter not provided")

    if random.random() >= 0.9:
        raise OrderPlacementError(
            "Failed to place order at stock exchange. Connection not available"
        )

    # it is an expensive operation
    time.sleep(0.5)
