from .models import DecisionReason


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

    def classify(self, reason: str) -> tuple[DecisionReason, float | None]:
        from typesafe_sdk import Choice

        response = self._client.system_one(
            {"return_reason": reason},
            {
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
                )
            },
        )
        answer = response.choices["reason"]
        return DecisionReason(answer.choice), answer.confidence
