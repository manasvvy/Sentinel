# Sentinel - Memory and Privacy

Status: Core safety and trust design

This document explains how Sentinel handles memory, what information is allowed to persist, and how privacy is enforced by design. Memory is treated as a system capability that requires explicit user control.

---

## Purpose

Memory increases usefulness, but it also increases risk.

Sentinel treats memory as optional, minimal, and explicit. The system prioritizes trust and safety over convenience.

This document answers:

* What Sentinel is allowed to remember
* What Sentinel must never remember
* How users control memory
* How memory interacts with confidence and safety

---

## Core principle

Sentinel does not remember people.

It remembers signals that help reduce future failure.

Memory exists to improve judgment, not personalization.

---

## Memory types

Sentinel uses two forms of memory:

* Short-term (session memory)
* Long-term (persistent memory)

Both are strictly scoped.

---

## Short-term memory (session only)

Short-term memory exists only for the duration of a single session.

It may include:

* Active topic
* Recent conversational turns
* Temporary context required for coherence

Short-term memory is cleared automatically when a session ends.

---

## Long-term memory (persistent, opt-in)

Long-term memory is stored only when the user explicitly allows it.

It may include:

* Topic-level corrections
* Confidence calibration by topic
* Indicators of where the system was corrected or uncertain
* Preferred explanation depth

Long-term memory is never applied automatically without consent.

---

## Explicitly forbidden storage

Sentinel must never store:

* Personal identifying information
* Emotional conversations or venting
* Raw message text
* Sensitive or private questions
* Information unrelated to system reliability

If information cannot be justified by safety or reliability, it is not stored.

---

## User control

Memory is always user-controlled.

Rules:

* Every session starts without memory applied
* Users choose whether the system may remember a session
* Memory can be manually reset at any time

The system never assumes consent.

---

## Anonymous but consistent identity

Sentinel uses anonymized identifiers to maintain consistency without identity.

* No PII is required
* Accounts are optional
* Identity exists only to associate memory safely

Consistency does not imply personalization.

---

## Relationship to confidence

Memory affects confidence, not content.

* Corrections reduce future confidence on the same topic
* Repeated uncertainty lowers baseline confidence
* Memory never forces answers or behavior

Confidence remains a system judgment, not a stored fact.

---

## Safety guarantees

Memory is designed to avoid:

* Creepy behavior
* False familiarity
* Referencing past emotional states
* Implicit surveillance

If a behavior feels invasive, it is a bug.

---

## What Sentinel does not do

* No silent memory
* No emotional profiling
* No long-term conversational recall
* No personalization based on private data

Memory is narrow by design.

---

Design principle: memory must be earned, minimal, and reversible.
