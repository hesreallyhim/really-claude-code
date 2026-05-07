---
name: TDD Squad Formation Exercise Overview
description: Explains the purpose, structure, and methodology of the TDD squad formation planning exercise.
---

# TDD Squad Formation Exercise: Overview

## What This Exercise Is

The TDD squad formation planning document (`tdd.md`) is a pre-specification planning document that works backward from a TDD squad deployment to define what the squads need to be. It is structured as a constraint-satisfaction problem.

## Structure

### 1. Inputs (Given)

A concrete project is classified along three axes:

- **Maturity level:** Prototype, Proof-of-concept, Steel Thread, MVP, V1, Enterprise-ready, Enterprise in high-regulation
- **Domain area:** Network reliance, Embedded systems, Security-related, Consumer tech
- **Timeline:** One week, One month, One quarter, One year

Plus a specification with clear acceptance criteria and functional/non-functional requirements.

### 2. Responsibilities (Must do)

Define what the squads are collectively responsible for. This is derived from how TDD methodology intersects with the given project classification. A prototype on a one-week timeline has very different TDD responsibilities than an enterprise-in-high-regulation project over a quarter.

### 3. Dependencies (Must have)

What capabilities, skills, tooling, and knowledge the squads need to fulfill those responsibilities. This is where skills like `scenario-architect` (for regulatory coverage), `testing-expert`, domain-specific knowledge, etc. get enumerated.

### 4. Squad composition (Will consist of)

Functional descriptions of each squad -- their purpose, topology, and coordination model.

### 5. Squad profiles (The squads)

References to individual Squad Formation Profile documents (using the template at `SQUAD-PROFILE.TEMPLATE.md`).

## Key Design Property

The document is **parametric** -- the same template gets filled out differently depending on which combination of maturity x domain x timeline is selected. The "enterprise in high-regulation" + "security-related" + "one quarter" combo produces radically different squad compositions than "prototype" + "consumer tech" + "one week."

## Purpose of the Unfilled Sections

The placeholder sections (`<STATE TEAM RESPONSIBILITIES>`, `<STATE TEAM DEPENDENCIES AND NEEDS>`, etc.) are prompts that enforce a **top-down derivation** rather than ad-hoc team assembly. The exercise requires reasoning through the dependencies before jumping to squad design.

## Companion Document: tdd-scenarios.md

The `tdd-scenarios.md` file provides 5 richly detailed project scenarios, each with a distinct parameter combination, generated using the `scenario-architect` skill. These scenarios serve as concrete inputs to drive the exercise -- each one can be fed into the `tdd.md` template to produce a different squad formation plan.
