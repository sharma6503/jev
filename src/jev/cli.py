import argparse
from datetime import date

from .agent import ReturnProcessingAgent
from .fixtures import DEFAULT_ORDERS, DEFAULT_POLICY
from .models import Resolution, ReturnRequest


def main() -> None:
    parser = argparse.ArgumentParser(description="Process an e-commerce return request.")
    parser.add_argument("order_id")
    parser.add_argument("item_id")
    parser.add_argument("resolution", choices=[Resolution.REFUND, Resolution.EXCHANGE])
    parser.add_argument("reason")
    parser.add_argument("--requested-on", default=date.today().isoformat())
    args = parser.parse_args()

    request = ReturnRequest(
        order_id=args.order_id,
        item_id=args.item_id,
        requested_resolution=Resolution(args.resolution),
        reason=args.reason,
        requested_on=date.fromisoformat(args.requested_on),
    )
    decision = ReturnProcessingAgent(DEFAULT_ORDERS, DEFAULT_POLICY).process(request)
    print(decision.message)


if __name__ == "__main__":
    main()
