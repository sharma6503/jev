# JEV Return Processing Agent Design

## Goal

Implement a deterministic Python return-processing agent for e-commerce return
requests. The first version must turn a request into an eligibility decision,
refund-or-exchange recommendation, and customer-facing response without
requiring external services or a language model.

## Scope

The agent accepts a typed `ReturnRequest` containing an order identifier,
item identifier, requested resolution, return reason, and request date. It
looks up typed in-memory order and policy fixtures, evaluates the request, and
returns a typed `ReturnDecision`.

The decision includes:

- eligibility: eligible or ineligible;
- explicit reason codes for missing orders, expired windows, non-returnable
  items, and unsupported requests;
- recommended resolution (`refund`, `exchange`, or `none`);
- a customer-facing response;
- enough structured context for callers to present or audit the result.

The initial policy uses a configurable return window, excludes non-returnable
items, and only permits refund or exchange when the item and order are found.
Fixtures are intentionally in memory and deterministic.

Jev is used only for the semantic part of the workflow: an optional
`ReasonClassifier` adapter maps free-form customer language to a small,
typed set of return reasons. Eligibility, policy enforcement, and side effects
remain deterministic code. The default fixture workflow can run without an API
key; callers opt into the Jev adapter when they need free-form reason
normalization.

## Architecture

The package is split into four focused layers:

1. **Domain models** define request, order, policy, and decision types.
2. **Repositories/fixtures** provide the in-memory order and policy data.
3. **Policy engine** evaluates eligibility and selects a resolution.
4. **Agent façade** coordinates lookup, evaluation, and response generation.

The public façade should be callable from Python and usable from a minimal
CLI entry point if the repository has no existing application convention.
The policy engine must not depend on presentation or CLI concerns.

## Error handling

Expected business failures are successful, structured decisions with an
ineligibility status and reason code. Malformed requests should fail
validation explicitly at the model boundary. No missing lookup or unknown
resolution should silently become an eligible return.

## Testing

Focused tests must cover:

- an eligible refund;
- an eligible exchange;
- an expired return window;
- a non-returnable item;
- a missing order or item;
- an unsupported resolution or malformed request;
- stable customer-facing response generation.

Tests should assert both structured fields and the important response text.
