from datetime import date

from .agent import ReturnProcessingAgent
from .fixtures import DEFAULT_ORDERS, DEFAULT_POLICY
from .models import Resolution, ReturnRequest
from .policy import KeywordReasonClassifier


def main() -> None:
    agent = ReturnProcessingAgent(
        DEFAULT_ORDERS,
        DEFAULT_POLICY,
        reason_classifier=KeywordReasonClassifier(),
    )
    examples = (
        ("Choice: damaged item", "The shirt arrived damaged"),
        ("Choice: changed mind", "I changed my mind about the color"),
        ("Hard rule: expired return", "The item no longer fits"),
    )

    for label, reason in examples:
        requested_on = date(2026, 10, 5) if "expired" in label else date(2026, 9, 20)
        decision = agent.process(
            ReturnRequest(
                order_id="ord-1001",
                item_id="sku-shirt",
                requested_resolution=Resolution.REFUND,
                reason=reason,
                requested_on=requested_on,
            )
        )
        print(label)
        print(f"  eligible: {decision.eligible}")
        print(f"  reason (Choice): {decision.reason_code.value}")
        print(f"  policy compliance (Noul): {decision.policy_compliance_probability}")
        print(f"  sentiment (Score): {decision.sentiment_score}")
        print(f"  sentiment confidence: {decision.sentiment_confidence}")
        print(f"  message: {decision.message}")
        print()


if __name__ == "__main__":
    main()
