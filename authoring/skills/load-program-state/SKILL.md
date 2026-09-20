---
name: load-program-state
description: Restore the program's canonical working state from the repository and identify exactly one authorized next action. Use at the start of a new session or after a handoff.
---

# Load program state

## Inputs

Follow `governance/state/LOAD-STATE.md`. Run `python tools/validate_state.py`,
then read `governance/state/current-state.yaml` and only its linked sources.

## Ownership

This skill is read-only. It does not own any repository file.

## Stop conditions

If validation fails, do not infer or start work; report the mismatch.

## Handoff

Report program mode, last accepted gate, module-state counts, debt with return
triggers, exactly one next action and unresolved external decisions.

## Lifecycle boundary

Do not update the manifest, choose a different action, start learner work, claim
proficiency or turn debt into an automatic authoring queue.
