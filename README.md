# Synthetic Catalog Reliability System

A public, synthetic reproduction of the reliability pattern used in a production catalog-ingestion platform. It contains no proprietary code, customer data, vendor data, or credentials.

The goal is to show how a catalog workflow can move from “the model extracted something” to “the system can measure, validate, repair, and route uncertainty.”

## What it does

- Reads synthetic supplier catalog records represented as model outputs.
- Normalizes safe aliases such as `nav` → `Navy` and `med` → `M`.
- Validates required fields and numeric ranges.
- Measures first-pass and final-pass success.
- Reports field-level accuracy.
- Routes missing or ambiguous values to human review.
- Produces a Markdown evaluation report.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
python catalog_reliability.py
```

No API key or external service is required.

## Architecture

```text
synthetic supplier record
          ↓
extraction result fixture
          ↓
canonicalization and validation
          ↓
bounded repair for safe aliases
          ↓
field-level evaluation
          ↓
publish / repair / human review
```

## Why this is synthetic

The production system that inspired this repository handled real supplier catalogs. This repository intentionally uses invented products and a small deterministic implementation so the method can be inspected and run publicly without exposing proprietary implementation details.

## Production boundary

A production implementation would add model adapters, prompt/model versioning, trace storage, privacy controls, cost/latency telemetry, retries with budgets, durable review queues, authentication, and integration with a retailer or PIM system.
