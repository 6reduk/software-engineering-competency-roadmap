---
name: audit-module-state
description: Audit curriculum module authoring readiness from accepted catalogs and artifacts. Use for explicit module-state decisions, not learner progress, proficiency, or automatic authoring selection.
---

# Audit module state

## Inputs

Read `governance/state/MODULE-STATE.md`, the relevant accepted module catalogs,
coverage maps, phase close-outs and acceptance decisions. Recount from sources;
do not infer readiness from old summaries alone.

## Ownership and work

Classify each defined module as `not-started`, `blueprint-only`, `partial`,
`ready-for-gate` or `closed-for-authoring` using the canonical definitions.
Record evidence, blocking debt, owner and observable return trigger. Tracks
without module definitions remain `track-skeleton-only`.

## Stop conditions

Stop the affected decision when accepted sources disagree, module boundaries are
undefined or the package does not authorize changing the canonical registry.

## Handoff and lifecycle boundary

Do not treat coverage, review, ImplementationReference, learner execution or
proficiency as interchangeable. Change module state only within an explicitly
authorized decision package. Handoff counts, transitions, evidence, debt and
the condition for the next audit; do not automatically select new authoring.
