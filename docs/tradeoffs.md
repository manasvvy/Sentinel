# Sentinel - Tradeoffs

Status: Explicit design decisions

This document outlines the major tradeoffs made while designing Sentinel. These decisions are intentional and reflect the project’s focus on safety, clarity, and system responsibility over scale or performance.

---

## Purpose

Every system makes tradeoffs.

Sentinel documents them explicitly to avoid accidental complexity and false expectations.

---

## API models over self-hosted models

Sentinel uses external LLM APIs rather than self-hosted or fine-tuned models.

Reasons:

* Focus remains on system behavior, not model optimization
* Reduced infrastructure and operational overhead
* Easier model replacement and comparison

Tradeoff:

* Less control over raw model behavior
* Dependency on third-party APIs

This choice keeps responsibility in the system layer.

---

## Simplicity over scale

Sentinel prioritizes correctness, safety, and clarity over throughput or concurrency.

Reasons:

* Complex systems hide failure
* Early optimization obscures responsibility
* Clear behavior is more valuable than high performance

Tradeoff:

* Not optimized for high-volume production traffic

---

## Manual review over automation (early stage)

Some governance actions require human judgment.

Reasons:

* Automated enforcement can amplify mistakes
* Early signals are often ambiguous
* Human review improves trust calibration

Tradeoff:

* Slower response to some failure patterns

Automation is deferred until behavior is well understood.

---

## Confidence signals over numeric scores

Sentinel communicates confidence as judgment, not probability.

Reasons:

* Numeric scores are often misinterpreted
* False precision increases over-trust
* Human-readable signals are more actionable

Tradeoff:

* Less granularity for quantitative analysis

---

## Limited memory by design

Sentinel intentionally restricts what it remembers.

Reasons:

* Memory increases risk
* Privacy violations erode trust quickly
* Most personalization is unnecessary for safety

Tradeoff:

* Reduced convenience and personalization

---

## No model training or retraining

Sentinel does not train or fine-tune models.

Reasons:

* Training shifts focus away from system behavior
* Retraining complicates accountability
* Corrections should affect confidence, not content

Tradeoff:

* Model limitations remain

---

## What Sentinel is not optimizing for

Sentinel explicitly does not optimize for:

* Maximum engagement
* Time spent in conversation
* Lowest possible latency
* Answer completeness at any cost

These metrics conflict with the project’s safety goals.

---

Design principle: clarity over capability.
