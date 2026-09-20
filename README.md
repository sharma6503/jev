# JEV

JEV is a typed e-commerce return-processing workflow. Deterministic Python
rules enforce return policy, while the Jev/TypeSafe SDK classifies free-form
customer return reasons.

## Run

```bash
pip install -e ".[test]"
pytest
jev-return ord-1001 sku-shirt refund "The shirt arrived damaged" --requested-on 2026-09-20
```

The same workflow is available through the Makefile:

```bash
make install
make check
make run
```

Set `TYPESAFE_API_KEY` before running the CLI or constructing
`ReturnProcessingAgent`; the agent uses `JevReasonClassifier()` by default.
For offline tests, explicitly inject `KeywordReasonClassifier()`.
