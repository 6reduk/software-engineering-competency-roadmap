---
name: correct-review-findings
description: Apply an orchestrator-approved set of review findings within explicit Ownership while preserving declared invariants. Do not use for broad rewrites, repeated review, or acceptance.
---

# Correct approved findings

## Inputs and stop conditions

Inputs must name the authoritative findings, dispositions, Ownership, protected
invariants and explicit non-changes. If any are missing or contradictory, stop
the affected correction and report the gap.

## Ownership and work

Snapshot the protected invariants before editing. Make the smallest changes that
close approved findings; Ownership is a maximum boundary, not a requirement to
touch every file. Do not add adjacent improvements, change coverage/metadata or
repeat Gate 0 unless explicitly authorized.

## Handoff and lifecycle boundary

Verify each finding by exact location or observable condition, then recheck
invariants, links, YAML and hygiene. Handoff a finding-to-change map, exact file
set, preserved invariants, checks and remaining dispositions. Keep materials in
their assigned lifecycle state and do not rerun review or declare acceptance.
