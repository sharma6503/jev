from datetime import date
from typing import Protocol

from .models import (
    DecisionReason,
    IneligibilityCode,
    Order,
    Resolution,
    ReturnDecision,
    ReturnItem,
    ReturnPolicy,
    ReturnRequest,
)


class ReasonClassifier(Protocol):
    def classify(self, reason: str) -> tuple[DecisionReason, float | None]:
        ...


class KeywordReasonClassifier:
    _KEYWORDS = {
        DecisionReason.DAMAGED: ("damaged", "broken", "arrived damaged"),
        DecisionReason.DEFECTIVE: ("defective", "doesn't work", "does not work"),
        DecisionReason.WRONG_ITEM: ("wrong item", "wrong size", "incorrect"),
        DecisionReason.CHANGED_MIND: ("changed my mind", "do not want", "don't want"),
    }

    def classify(self, reason: str) -> tuple[DecisionReason, float | None]:
        normalized = reason.casefold()
        for decision_reason, keywords in self._KEYWORDS.items():
            if any(keyword in normalized for keyword in keywords):
                return decision_reason, 1.0
        return DecisionReason.OTHER, 0.5


def evaluate_return(
    request: ReturnRequest,
    order: Order | None,
    policy: ReturnPolicy,
    reason_classifier: ReasonClassifier,
) -> ReturnDecision:
    if order is None:
        return _ineligible(request, IneligibilityCode.MISSING_ORDER, "We could not find that order.")

    item = order.item(request.item_id)
    if item is None:
        return _ineligible(request, IneligibilityCode.MISSING_ITEM, "We could not find that item on the order.")

    if not item.returnable:
        return _ineligible(
            request,
            IneligibilityCode.ITEM_NOT_RETURNABLE,
            f"{item.name} is not eligible for return under our policy.",
        )

    if not _within_return_window(item, request.requested_on, policy):
        return _ineligible(
            request,
            IneligibilityCode.RETURN_WINDOW_EXPIRED,
            "This return request is outside the return window.",
        )

    if request.requested_resolution not in (Resolution.REFUND, Resolution.EXCHANGE):
        return _ineligible(
            request,
            IneligibilityCode.UNSUPPORTED_RESOLUTION,
            "Please request either a refund or an exchange.",
        )

    reason, confidence = reason_classifier.classify(request.reason)
    resolution = request.requested_resolution
    action = "refund" if resolution == Resolution.REFUND else "exchange"
    return ReturnDecision(
        eligible=True,
        resolution=resolution,
        reason_code=reason,
        message=f"Your return is approved. We will process your {action} for {item.name}.",
        order_id=request.order_id,
        item_id=request.item_id,
        confidence=confidence,
    )


def _within_return_window(item: ReturnItem, requested_on: date, policy: ReturnPolicy) -> bool:
    return (requested_on - item.purchased_on).days <= policy.return_window_days


def _ineligible(
    request: ReturnRequest,
    reason: IneligibilityCode,
    message: str,
) -> ReturnDecision:
    return ReturnDecision(
        eligible=False,
        resolution=Resolution.NONE,
        reason_code=reason,
        message=message,
        order_id=request.order_id,
        item_id=request.item_id,
    )
