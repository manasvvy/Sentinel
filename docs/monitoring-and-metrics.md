# Sentinel - Monitoring and Metrics

Status: System evaluation and oversight

This document describes how Sentinel monitors behavior over time and evaluates whether the system is achieving its safety and trust goals. Monitoring focuses on patterns, not individual responses.

---

## Purpose

Sentinel does not optimize for raw accuracy.

It optimizes for safer usage, better judgment, and reduced over-trust. Monitoring exists to detect when the system is failing those goals.

This document answers:

* What Sentinel measures
* Why those signals matter
* How failure patterns are detected

---

## Core monitoring principle

Single answers are noisy.

Behavior over time is meaningful.

Sentinel evaluates trends, not isolated events.

---

## Primary metric

### User correction rate

The primary success signal for Sentinel is an increase in meaningful user corrections over time.

A higher correction rate indicates:

* Users are actively evaluating AI output
* Blind trust is decreasing
* Users feel safe challenging the system

A low correction rate combined with high confidence is treated as a risk signal.

---

## Supporting metrics

Sentinel tracks additional signals to understand system behavior:

* **Confident-wrong rate**
  Frequency of confident responses followed by user correction or contradiction.

* **Confidence vs correction mismatch**
  Cases where high confidence coincides with frequent correction.

* **Topic-level error recurrence**
  Repeated failures within the same topic area.

* **External verification acceptance**
  Whether users act on suggestions to verify answers externally.

* **Abandonment after incorrect answers**
  Sessions that end immediately after a detected failure.

---

## Drift detection

Sentinel monitors for behavioral drift rather than model drift alone.

Signals include:

* Rising correction frequency for previously stable topics
* Inconsistent outputs for similar prompts
* Sudden changes in confidence patterns

Drift is evaluated across time windows, not single sessions.

---

## Bias signals

Bias is treated as a pattern, not a label.

Sentinel monitors:

* Skewed responses across topics or categories
* Repeated user flags in similar contexts
* Systematic overconfidence in specific domains

Bias signals trigger review, not automatic suppression.

---

## Misuse detection

Sentinel monitors for abnormal usage patterns, including:

* Repeated unsafe prompts
* Attempts to bypass safety through rephrasing
* High-volume repetitive queries

Misuse signals inform governance decisions.

---

## Alerts and review

Monitoring outputs may trigger:

* Internal alerts
* Manual review
* Temporary confidence downgrades by topic

No automatic punitive action is taken against users.

---

## What Sentinel does not measure

* Raw model accuracy benchmarks
* Latency as a primary success metric
* Engagement or time spent as a goal

Sentinel values safer behavior over faster responses.

---

## Relationship to other systems

* Monitoring informs confidence calibration
* Monitoring feeds governance and audit logs
* Monitoring highlights areas requiring system improvement

Monitoring is a feedback loop, not a scoring system.

---

Design principle: measure what affects trust, not what is easy to count.
