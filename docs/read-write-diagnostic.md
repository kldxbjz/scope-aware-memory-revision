# Read versus write diagnostic
Source inspiration only: PairPref (https://arxiv.org/html/2609.34526v1) holds memory/request fixed while varying situations. We downloaded no PairPref examples and copied none. All six fixtures derive from our preexisting fictional paired_pilot families.

Run: `python3 -m unittest -v` and `python3 -m scope_memory.read_write_diagnostic`.
Results: `results/read_write_results.json` (the saved stdout).

## Isolation and denominators
Read-only: supply one correct controlled memory and identical request to two situations per family.
3 families / 6 requests / 3 pairs. Both sides must pass. No write operation.
Model-visible payload is only memory/request/situation; expected answers and variant labels are withheld.
Correct memory is intentionally supplied here to remove storage errors; this is not end-to-end learned memory evaluation.
Reader gets a fresh copy; mutation attempts are counted and cannot affect later calls.

Write-only: 3 families x 2 variants x 3 probes = 18.
Probe ordinary context before write, relevant context after write, ordinary context afterward.
Exception preserves default; durable update replaces default. The reader is fixed correct.
False overwrite denominator = 3 exception opportunities; missed update denominator = 3 durable-update opportunities.
Current writer controls use structured oracle transitions and are explicitly NOT learned or natural-language parsing.
When replacing controls with a trained writer, give only dialogue and prior predicted memory, not gold transitions.

## Deterministic negative controls (engineering checks, no scientific gain)
Correct read: 0/6 errors, 3/3 both-sides correct.
Overapply scoped memory everywhere: ordinary 3/3 errors, scoped 0/3, 0/3 pairs; zero writes.
Ignore scoped memory: scoped 3/3 errors, ordinary 0/3, 0/3 pairs; zero writes.
Persist exception as global: overwrite 3/3, missed update 0/3, probe errors 3/18.
Drop durable update: overwrite 0/3, missed update 3/3, probe errors 6/18.
Thus an identical bad ordinary-context answer can be attributed to read applicability versus corrupted state,
using a correct fixed-memory read test and independent state inspection rather than answer accuracy alone.

## Split / limitation
Both situation variants and exception/update controls stay in their original family split.
Only one family per split: suitable for plumbing, NOT sufficient evaluation or generalization evidence.
No training or measured model performance. Still blocked on verified observable labels and independently reviewed
examples spanning exception/update strata, then a bounded resource plan.

## Blind annotation checklist (proposal, not performed)
1. Hide graph attributes/change dates, generator tags and all future turns.
2. Show only observed prefix plus preexisting memory; mark precise evidence span.
3. Identify previous preference, new preference, scope, duration and whether replacement is explicit/inferable.
4. Label persistent revision / bounded exception / supported no-change / insufficient evidence.
5. Separate correct-memory read applicability from permission to write.
6. Same-time ordering uncertainty and missing earlier evidence force abstention.
7. Two teammates label independently before adjudication; report agreement and each denominator.
