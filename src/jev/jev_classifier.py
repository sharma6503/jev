from .models import DecisionReason, SemanticJudgments


class JevReasonClassifier:
    """Classifies free-form return language using TypeSafe's Jev model."""

    def __init__(self, client: object | None = None) -> None:
        if client is None:
            try:
                from typesafe_sdk import TypeSafeClient
            except ImportError as error:
                raise RuntimeError(
                    "Install JEV dependencies with `pip install -e .`."
                ) from error
            client = TypeSafeClient()
        self._client = client

    def classify(self, reason: str) -> SemanticJudgments:
        from typesafe_sdk import Choice, Noul, Score

        response = self._client.system_one(
            state=reason,
            questions={
                "reason": Choice(
                    instructions="Classify the customer's return reason.",
                    criteria={
                        "customer_request": "The customer asks to return without reporting a defect or fulfillment error.",
                        "damaged": "The item arrived physically damaged.",
                        "defective": "The item does not work or has a product defect.",
                        "wrong_item": "The customer received the wrong item or size.",
                        "changed_mind": "The customer no longer wants the item.",
                        "other": "None of the other categories apply.",
                    },
                ),
                "policy_compliant": Noul(
                    instructions="Would this return request normally comply with the stated return policy?",
                ),
                "sentiment": Score(
                    instructions="How emotionally intense is the customer's return message?",
                    criteria=[
                        "Calm and factual",
                        "Frustrated but civil",
                        "Very angry or threatening to leave",
                    ],
                ),
            },
        )
        reason_answer = response.answers["reason"]
        policy_answer = response.answers["policy_compliant"]
        sentiment_answer = response.answers["sentiment"]
        return SemanticJudgments(
            reason=DecisionReason(reason_answer.choice),
            reason_confidence=reason_answer.confidence,
            policy_compliance_probability=policy_answer.noul,
            sentiment_score=sentiment_answer.score,
            sentiment_confidence=sentiment_answer.confidence,
        )
