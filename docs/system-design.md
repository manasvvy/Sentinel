# Sentinel - System Design

Status: Conceptual system design (implementation in progress)

Sentinel is a backend‑centric system that wraps external LLM APIs with confidence logic, memory (with consent), monitoring, and governance. The model is a dependency. Responsibility lives in the system.

This document focuses on how Sentinel is designed, not how it is marketed.

---

## Design goals

Sentinel is designed to solve system‑level failure, not model‑level performance.

Primary goals:

* Prevent confident‑wrong behavior
* Make uncertainty explicit and visible
* Enable meaningful human correction
* Preserve privacy by default
* Embed governance without harming conversational UX

Explicit non‑goals:

* Training or hosting models
* Optimizing for speed or smoothness
* Storing personal or emotional data

---

## High‑level architecture

User
→ Frontend (UI only)
→ Backend API
→ Confidence and safety logic
→ Memory and state
→ Logs and monitoring
→ External LLM API

Mental model:

* Frontend: mouth and ears
* Backend: brain and rules
* Model API: external intelligence
* Database: memory
* Logs: CCTV

The model does not live in Sentinel. Sentinel owns responsibility.

---

## Component responsibilities

Frontend

* Collect user input
* Display responses and confidence state
* Offer optional clarification or “why” affordances
* No memory, safety, or decision logic

Backend API (FastAPI)

* Session handling
* Context assembly
* Confidence evaluation
* Safety and governance checks
* Memory orchestration (opt‑in only)
* Structured logging

AI model API

* Stateless text generation
* Fully replaceable dependency
* Never trusted blindly

Database

* Short‑term and long‑term memory
* User‑controlled persistence
* No raw message storage

Logs and metrics

* Append‑only interaction records
* Auditability and monitoring over time

---

## Identity and sessions

Identity

* Anonymous but consistent identifiers
* Optional account wrapper
* No PII required

Sessions

* Every chat starts fresh
* Past chats are visible but not auto‑loaded
* Memory is applied only with explicit consent per session

---

## End‑to‑end data flow

1. User submits input via the frontend
2. Frontend sends request with session_id and anonymized user_id
3. Backend validates input and applies safety pre‑checks
4. Backend assembles context (session context + approved memory)
5. Backend calls the external LLM API
6. Model returns a response
7. Backend evaluates confidence and applies governance rules
8. Backend logs the interaction and updates memory if allowed
9. Frontend displays the response with confidence signal

---

## Confidence logic

Sentinel does not expose probabilities. It exposes judgment.

Confidence states:

* Confident
* Guessing

Signals used to evaluate confidence:

* Presence of reasoning
* Explicit limitations
* Consistency across turns
* Alignment with known or prior knowledge
* Self‑contradiction or topic drift

Rules:

* Confidence may change mid‑answer
* Overconfidence is penalized harder than uncertainty
* Confidence is lost faster than it is earned

When confidence is low:

* Ask clarifying questions
* Suggest external verification
* Avoid looping on “best possible answer” refinement

---

## Memory model

Short‑term (session only)

* Active topic
* Recent turns
* Temporary context

Long‑term (persistent, safe)

* Topic‑level corrections
* Confidence calibration by topic
* Indicators of strength or struggle
* Explanation depth preference

Explicitly forbidden:

* Personal information
* Emotional conversations
* Raw message text
* Sensitive questions

Memory control:

* Manual reset only
* Explicit user consent per session

---

## Corrections and learning

User corrections are treated as first‑class signals.

* Corrections are logged at the topic level
* Future confidence for that topic is reduced
* Content is not blindly overwritten
* Corrections inform monitoring and governance, not instant retraining

---

## Governance and safety

Sentinel separates experience from enforcement.

* UX layer: conversational and flexible
* Safety layer: deterministic and rule‑based

Safety never negotiates with UX.

Explainability:

* Human‑readable explanations on demand
* No raw probability exposure

---

## Logging and auditability

Each interaction logs:

* Timestamp
* Anonymized user_id
* Session_id
* Confidence state
* Flags (bias, drift, misuse)
* User action (accepted or corrected)

Logs exist for debugging, audits, and accountability.

---

## Monitoring and metrics

Sentinel measures behavior, not just outputs.

Primary metric:

* Increase in meaningful user corrections over time

Supporting metrics:

* Confident‑wrong rate
* Confidence vs correction mismatch
* Topic‑level error recurrence
* External verification acceptance
* Abandonment after incorrect answers

Monitoring focuses on patterns, not single events.

---

## Drift, bias, and misuse

Drift

* Rising correction frequency
* Inconsistent outputs for similar inputs

Bias

* Skewed responses across topics or user groups
* Repeated user flags

Misuse

* Repeated unsafe prompts
* Abnormal usage patterns

---

## Tradeoffs

* Simplicity over scale
* API models over self‑hosted models
* Manual review over automation (early stage)
* Correctness before performance

---

## Future direction

* Automated bias evaluation
* Richer confidence calibration
* Scalable monitoring pipelines
* Model version comparison

---

Design principle: never hide uncertainty.
