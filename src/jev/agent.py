from collections.abc import Iterable

from .models import Order, ReturnDecision, ReturnPolicy, ReturnRequest
from .policy import KeywordReasonClassifier, ReasonClassifier, evaluate_return


class ReturnProcessingAgent:
    def __init__(
        self,
        orders: Iterable[Order],
        policy: ReturnPolicy,
        reason_classifier: ReasonClassifier | None = None,
    ) -> None:
        self._orders = {order.order_id: order for order in orders}
        self._policy = policy
        self._reason_classifier = reason_classifier or KeywordReasonClassifier()

    def process(self, request: ReturnRequest) -> ReturnDecision:
        return evaluate_return(
            request=request,
            order=self._orders.get(request.order_id),
            policy=self._policy,
            reason_classifier=self._reason_classifier,
        )
