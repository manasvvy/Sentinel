# Sentinel - Confidence Logic

Status: Core system behavior

This document explains how Sentinel evaluates confidence, communicates uncertainty, and handles confident-wrong behavior. This is a system-level mechanism, not a model capability.

---

## Purpose

Sentinel exists to prevent over-trust.

Confidence logic is the primary way the system slows AI down enough for humans to think.

This document answers:

* What “confident” and “guessing” mean in Sentinel
* How confidence is evaluated
* How confidence changes during a response
* What the system does when confidence is low or wrong

---

## Design principle

Sentinel does not expose probabilities.

Probabilities are misleading for users and create a false sense of precision. Instead, Sentinel exposes **judgment** in a human-readable form.

Uncertainty must be explicit. Overconfidence is treated as a failure state.

---

## Confidence states

Sentinel uses two explicit states:

* **Confident**
* **Guessing**

These states are mutually exclusive and visible to the user.

---

## What “confident” means

A response is marked confident when the system determines that:

* The model provides clear reasoning
* Limitations or assumptions are acknowledged
* The response remains internally consistent
* The answer aligns with known or previously validated knowledge

Confidence is never absolute. It reflects system judgment, not truth.

---

## What “guessing” means

A response is marked guessing when:

* The model lacks sufficient context
* The answer relies on weak or generic reasoning
* The response shifts direction mid-way
* The system detects possible hallucination or topic drift

Guessing is not a failure. Pretending not to guess is.

---

## Signals used for evaluation

Sentinel evaluates confidence using multiple signals:

* Presence of step-by-step reasoning
* Explicit statements of limitation or uncertainty
* Consistency across turns in the same session
* Stability when the same question is rephrased or repeated
* Alignment with prior validated corrections
* Detection of contradiction or topic drift

No single signal is decisive. Confidence is a composite judgment.

---

## Confidence changes mid-response

Sentinel allows confidence to change within a single response.

If the model starts with strong reasoning but later enters uncertain territory, the system downgrades confidence rather than forcing consistency.

This avoids false confidence and reflects real reasoning behavior.

---

## Handling low confidence

When a response is marked guessing, Sentinel may:

* Ask clarifying questions
* Narrow the scope of the answer
* Suggest external verification

Sentinel does not loop endlessly trying to refine the “best” answer.

---

## Confident-wrong behavior

Confident-wrong responses are treated as the most serious failure mode.

When detected:

* Confidence is downgraded aggressively
* The interaction is flagged in logs
* Future confidence on the same topic is reduced

Repeated confident-wrong patterns trigger monitoring alerts.

---

## User corrections

User corrections are first-class signals.

When a user corrects the system:

* The correction is logged at the topic level
* The system reduces future confidence for that topic
* Content is not overwritten blindly

Corrections inform system behavior, not instant retraining.

---

## What Sentinel does not do

* No numeric confidence scores
* No probability percentages
* No pretending to “know” when it does not

Confidence is communicated clearly or not at all.

---

## Relationship to other components

* Confidence logic informs memory updates
* Confidence signals affect monitoring metrics
* Confidence failures trigger governance review

Confidence is the connective tissue between UX, memory, and safety.

---

Design principle: never hide uncertainty.
