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
make setup
make check
make run
```

Use `.env.example` as a template and export `TYPESAFE_API_KEY` in your shell
before running the CLI or constructing `ReturnProcessingAgent`. The SDK uses
the `jev-latest` model by default; set `TYPESAFE_DEFAULT_MODEL` to override it.
Each semantic evaluation uses a TypeSafe Choice for reason category, a Noul
for policy compliance, and a Score for customer sentiment. Hard order and
return-window rules remain deterministic.
For offline tests, explicitly inject `KeywordReasonClassifier()`.
