# Scope-Aware Memory Revision: synthetic SFT tranche v0.1

**160 authored synthetic transition examples, not a trained result or natural-data benchmark.** Generated locally without an LLM/API, GPU, remote write, or training. Labels follow construction rules; structural checks are not independent semantic validation.

## Contents and commands

- `build.py`: deterministic source, 40 domain/value/scope specifications and 10 discourse families.
- `inputs.jsonl`: 160 visible episodes plus bookkeeping IDs/split assignments.
- `labels.jsonl`: canonical pre/post states, transition, action and decision labels; never concatenate this file into model inputs.
- `crud_sft.jsonl`, `scope_sft.jsonl`: paired SFT rows `{id,split,prompt,completion}`. **Prompt strings are byte-identical across arms.** Bookkeeping fields are not part of prompt.
- `manifest.json`: record/action/split counts and SHA-256 hashes of all four JSONL files.
- `validate.py`: CPU-only invariant checks.

Run `python scope_revision_training/build.py && python scope_revision_training/validate.py` from the workspace parent. No external dependency required.

## Generation and chronology

Specify initial durable state first, choose one of four transitions, derive post-state, then render a three-turn user/assistant/user episode. Memory is the snapshot **before** the first visible turn. The conversation list is chronological; it is not a whole-life trajectory, has no synthetic timestamps, and must not be advertised as free-running multi-write replay. The assistant asks a neutral value question; the final user specifies the new value. Four examples for each domain share exact initial memory, assistant turn, and final user turn; earlier user intent distinguishes the correct action. In unresolved cases the user explicitly requires a scope question before saving; providing a value later does not resolve scope.

- `set_default`: replace ordinary default, preserve existing scoped records.
- `set_exception`: add or replace rule in the named context, preserve default.
- `no_op`: satisfy an ephemeral request without changing durable memory.
- `defer`: leave memory unchanged and request scope clarification before any write.

There are 40 per action. Twenty exception examples replace an existing scoped record, twenty add one. The pre-existing scoped rule currently has the same value as the initial default; its explicit scoped identity remains meaningful when the default changes. No example deletes an exception.

## Schema and paired arms

`inputs.input.memory` is a list of free-text records `{id,text}`. It can express both a default and any scoped exception; CRUD is **not** restricted to a single unscoped slot. `inputs.input.conversation` contains `{role,content}` records. The prompt has only those memory and conversation objects, no action, gold state, split, domain-family or contrast label.

`labels.pre_state/post_state = {default: string, exceptions: {scope: value}}`. `change` is null or `{kind: default, value}` / `{kind: exception, scope, value}`. Canonical text is rendered by one shared function; tests ensure both views agree and applying each completion reproduces the target text/state exactly.

Scope completion: `{action,change,decision}`.
CRUD completion: `{operations:[{op:add|update,record:{id,text}} | {op:no_op}],decision}`.
`decision` is `resolved` or `clarify_before_saving`, allowing CRUD to distinguish clarification from an ordinary no-op rather than penalizing its representation. It records a clarification decision, not actual natural-language response quality. CRUD instructions should allow add/update/delete/no-op broadly, although delete has zero training examples in this tranche. Each arm needs a fixed external task/schema instruction; the stored evidence prompt remains identical. Both arms must use equal model/training budgets. Do not train using labels or gold post-state as input.

## Split and isolation

128 train / 32 development, each split balanced across all four actions. Forty domain contrast groups are intact. Discourse families t00–t07 are train; t08–t09 are development, including their intent wording, not merely a different final-turn paraphrase. Domains and template IDs are disjoint across splits. **All ten families still share a common generation mechanism and explicit intent taxonomy. Their stylistic differences are not independent natural distributions.** Random record-level splitting would leak matched families and is forbidden.

Prior 40-example pilot and 24-example held-out set were not ingested as training examples; their named domain inventories were inspected and avoided. This does not establish semantic disjointness across all broader activities (e.g., visual preferences). The earlier held-out set must remain frozen and excluded from training/selection.

## Limits and next evaluation

This is a small, deliberately easy warm-start tranche: intent is unusually explicit, exactly three turns per record, one preference domain and one scope at most, no contradictory evidence, implicit scope, stale references, deletion, or interacting overlapping scopes. Instruction recognition may solve it without learning general memory revision. Domain values are fictional and include awkward edge cases; no claim of human verification. Count 160 records is not 160 independent semantic problems: there are 40 matched groups and only 10 authored discourse families.

Use development only for implementation checks and selection, not a paper-level generalization claim. Report suffix-only and assistant-only probes, matched-group success, action confusion, exact state accuracy, default-preservation and exception-preservation. Actual scientific validation needs multi-write chronological free-running evaluation on a frozen independent set, using each model's own prior memory, paired ordinary/scoped QA and false-overwrite measurements. This package creates no learned model and reports no learned accuracy.
