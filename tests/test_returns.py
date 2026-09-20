from datetime import date

import pytest

from jev.agent import ReturnProcessingAgent
from jev.fixtures import DEFAULT_ORDERS, DEFAULT_POLICY
from jev.models import IneligibilityCode, Resolution, ReturnRequest
from jev.policy import KeywordReasonClassifier


def request(**overrides: object) -> ReturnRequest:
    values: dict[str, object] = {
        "order_id": "ord-1001",
        "item_id": "sku-shirt",
        "requested_resolution": Resolution.REFUND,
        "reason": "The color is not right",
        "requested_on": date(2026, 9, 20),
    }
    values.update(overrides)
    return ReturnRequest(**values)


@pytest.fixture
def agent() -> ReturnProcessingAgent:
    return ReturnProcessingAgent(
        DEFAULT_ORDERS,
        DEFAULT_POLICY,
        reason_classifier=KeywordReasonClassifier(),
    )


def test_approves_refund_and_classifies_reason(agent: ReturnProcessingAgent) -> None:
    decision = agent.process(request(reason="The shirt arrived damaged"))
    assert decision.eligible is True
    assert decision.resolution == Resolution.REFUND
    assert decision.reason_code.value == "damaged"
    assert "refund" in decision.message
    assert decision.policy_compliance_probability == 1.0
    assert decision.sentiment_score == 1.0
    assert decision.sentiment_confidence == 1.0


def test_approves_exchange(agent: ReturnProcessingAgent) -> None:
    decision = agent.process(request(requested_resolution=Resolution.EXCHANGE))
    assert decision.eligible is True
    assert decision.resolution == Resolution.EXCHANGE
    assert "exchange" in decision.message


def test_rejects_expired_return(agent: ReturnProcessingAgent) -> None:
    decision = agent.process(request(requested_on=date(2026, 10, 5)))
    assert decision.eligible is False
    assert decision.reason_code == IneligibilityCode.RETURN_WINDOW_EXPIRED


def test_rejects_non_returnable_item(agent: ReturnProcessingAgent) -> None:
    decision = agent.process(
        request(order_id="ord-1002", item_id="sku-earrings")
    )
    assert decision.reason_code == IneligibilityCode.ITEM_NOT_RETURNABLE


def test_rejects_missing_order(agent: ReturnProcessingAgent) -> None:
    decision = agent.process(request(order_id="missing"))
    assert decision.reason_code == IneligibilityCode.MISSING_ORDER


def test_rejects_unsupported_resolution(agent: ReturnProcessingAgent) -> None:
    decision = agent.process(request(requested_resolution=Resolution.NONE))
    assert decision.reason_code == IneligibilityCode.UNSUPPORTED_RESOLUTION


def test_validates_required_fields() -> None:
    with pytest.raises(ValueError, match="reason is required"):
        request(reason=" ")


def test_jev_classifier_reads_quickstart_response_shape() -> None:
    from jev.jev_classifier import JevReasonClassifier

    class Answer:
        choice = "damaged"
        confidence = 0.9

    class NoulAnswer:
        noul = 0.8

    class ScoreAnswer:
        score = 1.25
        confidence = 0.7

    class FakeClient:
        def system_one(self, *, state: str, questions: dict[str, object]) -> object:
            assert state == "The item arrived damaged"
            assert set(questions) == {"reason", "policy_compliant", "sentiment"}

            class Response:
                answers = {
                    "reason": Answer(),
                    "policy_compliant": NoulAnswer(),
                    "sentiment": ScoreAnswer(),
                }

            return Response()

    classifier = JevReasonClassifier(client=FakeClient())
    judgments = classifier.classify("The item arrived damaged")
    assert judgments.reason.value == "damaged"
    assert judgments.reason_confidence == 0.9
    assert judgments.policy_compliance_probability == 0.8
    assert judgments.sentiment_score == 1.25
    assert judgments.sentiment_confidence == 0.7
