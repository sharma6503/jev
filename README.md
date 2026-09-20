# JEV

JEV is a typed e-commerce return-processing workflow. Deterministic Python
rules enforce return policy, while the optional Jev/TypeSafe adapter can
classify free-form customer return reasons.

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

Install the optional TypeSafe integration with `pip install -e ".[jev]"`, then
inject `JevReasonClassifier()` into `ReturnProcessingAgent` when processing
free-form reasons. The default keyword classifier requires no API key.