# First paired SFT experiment: design, not launched
Prerequisite: verified observable action dataset with two annotators and adjudication; enough true updates and scoped exceptions to estimate both error rates.
Audit users are excluded from final evaluation and training. Freeze user-disjoint manifests before deriving examples; group all timeline variants/generator duplicates by user. Keep LongMemEval and MemSyco-Bench as untouched external tests; never tune on their gold fields or QA.
Use same base checkpoint, tokenizer, user examples, context evidence, memory token limit, optimizer, adapter rank, steps, effective tokens, seeds (3), compute cap and hyperparameter-selection budget for both arms.
Baseline: generic CRUD over free-text memories; allow it to express context in free text (not the toy scope-blind overwrite rule).
Proposed: CRUD plus explicit scope/relation schema. Match available memory capacity and serialized tokens; report structured-output overhead.
Both learn action labels from identical verified examples; neither receives gold scope/action/graph at inference. Evaluate predicted memory rollouts, not teacher-forced oracle memories. Use the same frozen QA reader and decoding.
Primary: paired preference QA; false-overwrite rate on verified exception opportunities; missed-true-update rate on verified persistent-update opportunities. Report exact denominators, abstentions, invalid actions, memory tokens and latency.
Bootstrap users (not turns), show 95% paired confidence intervals across users and seed variation separately.
Hold fixed selection rules before final test. Add capacity-matched structured-control ablation if affordable; separate schema gains from learning.
Resource plan and model choice remain UNSET pending local model availability, data readiness, and an explicit bounded training plan. No training, GPUs or paid generation launched.
