from datetime import date

from .models import Order, ReturnItem, ReturnPolicy


DEFAULT_POLICY = ReturnPolicy(return_window_days=30)

DEFAULT_ORDERS: tuple[Order, ...] = (
    Order(
        order_id="ord-1001",
        items=(
            ReturnItem(
                item_id="sku-shirt",
                name="Cotton shirt",
                purchased_on=date(2026, 9, 1),
                price=3500,
            ),
        ),
    ),
    Order(
        order_id="ord-1002",
        items=(
            ReturnItem(
                item_id="sku-earrings",
                name="Gold earrings",
                purchased_on=date(2026, 7, 1),
                price=8900,
                returnable=False,
            ),
        ),
    ),
)
