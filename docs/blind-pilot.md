# Internal blind annotation pilot
12 fictional, author-written episodes: 4 topic/template families x 3 labels.
4 lasting updates, 4 scoped exceptions, 4 insufficient/ambiguous statements.
No HorizonBench or PairPref dialogue copied. No dataset/model API call.

## Separation and process
`annotations/blind_pilot/blind_packet.json` contains instructions, opaque IDs and user messages only.
`annotations/blind_pilot/blind_gold.json` is the separate author key plus family/split manifest. Do not pass it to an annotator/model.
Two fresh internal subagents received only texts and the label rubric, no parent history, files, tools or author key.
A saw shuffled aliases a-l; B saw original 01-12 order. Both returned locked labels before comparison.
`annotations/blind_pilot/blind_locked_labels.json` records exact locked categories and A's alias mapping. Brief explanations in each
pass confirmed explicit duration/replacement cues versus tentative interest, reported suggestions or past success.
No adjudication changes required: 12/12 agreement; 12/12 each against author key, 4/4 in each class.

## Interpretation / readiness
This is internal same-model agreement on very easy explicit templates, NOT independent human agreement,
not evidence of model training/generalization, and not validation of naturally occurring ambiguous timelines.
Prompt order differed, but agents shared the same underlying model and rubric; correlated mistakes remain possible.
Template cues strongly reveal labels. Do not use these results as scientific accuracy.
Family split: format/schedule train, drink validation, travel test; all three variants stay together.
This tiny 6/3/3 split is plumbing only; broad paraphrase/template diversity and real observations still required.

Decision: evaluation and annotation plumbing ready; scientific training data NOT ready.
Next gate: enlarge verified examples across multiple scopes/durations, blind independent teammate review
and adjudication, exact evidence spans, balanced error strata, then freeze user/template-disjoint split and
bounded training plan. No outreach, training, GPU, paid calls or push performed.

Reproduce: `python3 -m unittest -v` and `python3 -m scope_memory.score_blind_pilot` (stdout saved as `results/blind_score.json`).
