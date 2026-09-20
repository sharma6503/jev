from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import StrEnum


class Resolution(StrEnum):
    REFUND = "refund"
    EXCHANGE = "exchange"
    NONE = "none"


class IneligibilityCode(StrEnum):
    MISSING_ORDER = "missing_order"
    MISSING_ITEM = "missing_item"
    RETURN_WINDOW_EXPIRED = "return_window_expired"
    ITEM_NOT_RETURNABLE = "item_not_returnable"
    UNSUPPORTED_RESOLUTION = "unsupported_resolution"


class DecisionReason(StrEnum):
    CUSTOMER_REQUEST = "customer_request"
    DAMAGED = "damaged"
    DEFECTIVE = "defective"
    WRONG_ITEM = "wrong_item"
    CHANGED_MIND = "changed_mind"
    OTHER = "other"


@dataclass(frozen=True)
class ReturnRequest:
    order_id: str
    item_id: str
    requested_resolution: Resolution
    reason: str
    requested_on: date

    def __post_init__(self) -> None:
        if not self.order_id.strip() or not self.item_id.strip():
            raise ValueError("order_id and item_id are required")
        if not self.reason.strip():
            raise ValueError("reason is required")


@dataclass(frozen=True)
class ReturnItem:
    item_id: str
    name: str
    purchased_on: date
    price: int
    returnable: bool = True


@dataclass(frozen=True)
class Order:
    order_id: str
    items: tuple[ReturnItem, ...]

    def item(self, item_id: str) -> ReturnItem | None:
        return next((item for item in self.items if item.item_id == item_id), None)


@dataclass(frozen=True)
class ReturnPolicy:
    return_window_days: int = 30

    def __post_init__(self) -> None:
        if self.return_window_days < 0:
            raise ValueError("return_window_days cannot be negative")


@dataclass(frozen=True)
class ReturnDecision:
    eligible: bool
    resolution: Resolution
    reason_code: DecisionReason | IneligibilityCode
    message: str
    order_id: str
    item_id: str
    confidence: float | None = None
