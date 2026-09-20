# JEV

JEV is a typed e-commerce return-processing workflow. Deterministic Python
rules enforce return policy, while the Jev/TypeSafe SDK classifies free-form
customer return reasons.

## Run

```bash
uv sync --extra test
uv run pytest
uv run jev-return ord-1001 sku-shirt refund "The shirt arrived damaged" --requested-on 2026-09-20
```

The same workflow is available through the Makefile:

```bash
make setup
make check
make run
make examples
```

`uv` is the primary environment and package manager. If `uv` is unavailable,
the equivalent fallback is `pip install -e ".[test]"`, followed by the same
commands through the installed Python environment.

Use `.env.example` as a template and export `TYPESAFE_API_KEY` in your shell
before running the CLI or constructing `ReturnProcessingAgent`. The SDK uses
the `jev-latest` model by default; set `TYPESAFE_DEFAULT_MODEL` to override it.
Each semantic evaluation uses a TypeSafe Choice for reason category, a Noul
for policy compliance, and a Score for customer sentiment. Hard order and
return-window rules remain deterministic.
For offline tests, explicitly inject `KeywordReasonClassifier()`.

## Logic examples

Run the complete offline example set with `make examples`. It demonstrates:

- **Choice:** classifies a free-form reason such as “The shirt arrived
  damaged” as `damaged`.
- **Noul:** returns a policy-compliance probability for the request.
- **Score:** returns customer sentiment intensity on a three-level scale.
- **Deterministic rules:** rejects an expired return even when semantic
  judgments are available.

The examples use `KeywordReasonClassifier()` so they do not require
`TYPESAFE_API_KEY`. Production processing uses `JevReasonClassifier()` by
default and obtains the same three typed judgments from the TypeSafe SDK.
