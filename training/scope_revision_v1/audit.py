#!/usr/bin/env python3
"""Deterministic, offline diagnostics for protocol-v1 episode JSONL files.

This is an audit, not a proof of semantic correctness or model difficulty.
``audit(data_dir)`` is side-effect free; the CLI writes data_dir/audit.json.
Only Python's standard library is used. No IDs, labels, rationales, memory, or
probes enter the last-user classifier or the contrast suffix features.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
import re
import unicodedata

SPLITS = ("train", "dev", "test")
CATEGORIES = (
    "general_update", "scoped_exception", "exception_revision",
    "exception_retirement", "stable_preference", "clarify",
)
WRITE_CATEGORIES = frozenset(CATEGORIES[:4])
BROAD_CLASSES = {
    "general_update": "General Update",
    "scoped_exception": "Scoped Exception",
    "exception_revision": "Exception Revision",
    "exception_retirement": "Exception Revision",
    "stable_preference": "Stable Preference",
    "clarify": "Stable Preference",
}
PROBE_TYPES = ("target", "default", "neighbor", "boundary")
KEYWORDS = ("exception", "default", "usual", "always", "only", "for now",
            "temporary", "one-off", "remember", "save")
WORD_RE = re.compile(r"[a-z0-9]+(?:'[a-z0-9]+)*")
NORMALIZATION = (
    "Unicode NFKC, curly apostrophes replaced with straight apostrophes, "
    "casefold, then [a-z0-9]+(?:'[a-z0-9]+)* tokens. Punctuation separates "
    "words; one-off is the two-token phrase 'one off'. No stemming. "
    "N-grams never cross message boundaries."
)


def words(text):
    return WORD_RE.findall(unicodedata.normalize("NFKC", text)
                           .replace("\u2019", "'").replace("\u2018", "'").casefold())


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def read_jsonl(path):
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def events(episodes):
    for episode in episodes:
        for event in episode["events"]:
            yield episode, event


def last_user(event):
    return next((message["content"] for message in reversed(event["dialogue"])
                 if message["role"] == "user"), "")


def ratio(numerator, denominator):
    return numerator / denominator if denominator else None


def complete(counter, keys):
    return {key: counter[key] for key in keys}


def sorted_counts(counter):
    return {str(key): counter[key] for key in sorted(counter, key=str)}


def dataset_counts(episodes):
    category = Counter()
    decisions = Counter()
    roles = Counter()
    event_lengths = Counter()
    dialogue_lengths = Counter()
    evidence_positions = Counter()
    validity_snapshots = Counter()
    validity_changes = Counter()
    probe_categories = Counter()
    probe_types = Counter()
    probe_broad = Counter()
    probe_cross = {name: Counter() for name in dict.fromkeys(BROAD_CLASSES.values())}
    probed_events = Counter()
    attributes, values, scopes, families = set(), set(), set(), set()
    total_messages = total_tokens = total_probes = 0
    for episode in episodes:
        event_lengths[len(episode["events"])] += 1
        families.add(episode["family"])
        for catalog in episode["attributes"]:
            attributes.add(catalog["attribute"])
            values.update(catalog["options"])
            for scope in catalog["scopes"].values():
                scopes.add(scope["scope"])
                scopes.update(scope.get("aliases", []))
        previous = episode["initial_state"]
        for event in episode["events"]:
            gold = event["gold"]
            category[gold["category"]] += 1
            decisions[gold["decision"]] += 1
            dialogue_lengths[len(event["dialogue"])] += 1
            evidence_positions[gold["evidence_message"]] += 1
            for message in event["dialogue"]:
                roles[message["role"]] += 1
                total_tokens += len(words(message["content"]))
                total_messages += 1
            for attribute, state in gold["state_after"].items():
                before = previous.get(attribute, {}).get("exceptions", {})
                for scope_key, record in state["exceptions"].items():
                    kind = record["validity"]["kind"]
                    validity_snapshots[kind] += 1
                    if before.get(scope_key) != record:
                        validity_changes[kind] += 1
            previous = gold["state_after"]
        probed_events[len({probe["after_event"] for probe in episode["probes"]})] += 1
        for probe in episode["probes"]:
            total_probes += 1
            cat, ptype = probe["category"], probe["probe_type"]
            broad = BROAD_CLASSES.get(cat, "UNKNOWN:" + cat)
            probe_categories[cat] += 1
            probe_types[ptype] += 1
            probe_broad[broad] += 1
            probe_cross.setdefault(broad, Counter())[ptype] += 1
    return {
        "episodes": len(episodes), "events": sum(category.values()),
        "messages": total_messages, "normalized_word_tokens": total_tokens,
        "event_categories": complete(category, CATEGORIES),
        "decisions": sorted_counts(decisions),
        "write_events": sum(category[c] for c in WRITE_CATEGORIES),
        "no_write_events": category["stable_preference"] + category["clarify"],
        "message_roles": sorted_counts(roles),
        "events_per_episode": sorted_counts(event_lengths),
        "messages_per_event": sorted_counts(dialogue_lengths),
        "evidence_message_positions": sorted_counts(evidence_positions),
        "qa_probes": total_probes,
        "qa_by_category": complete(probe_categories, CATEGORIES),
        "qa_by_broad_class": complete(probe_broad, dict.fromkeys(BROAD_CLASSES.values())),
        "qa_by_type": complete(probe_types, PROBE_TYPES),
        "qa_by_broad_class_and_type": {
            broad: complete(counts, PROBE_TYPES) for broad, counts in probe_cross.items()},
        "probed_events_per_episode": sorted_counts(probed_events),
        "validity_active_record_snapshots": complete(validity_snapshots, ("persistent", "window", "open")),
        "validity_new_or_revised_records": complete(validity_changes, ("persistent", "window", "open")),
        "distinct_attributes": len(attributes), "distinct_values": len(values),
        "distinct_scope_phrases_including_aliases": len(scopes),
        "distinct_families": len(families),
    }


class NaiveBayes:
    """Multinomial word-count NB; alpha=1, empirical add-one class priors."""
    def __init__(self, train_rows, labels=CATEGORIES):
        self.labels = tuple(labels)
        self.class_counts = Counter()
        self.token_counts = {label: Counter() for label in self.labels}
        self.vocabulary = set()
        for text, label in train_rows:
            tokens = words(text)
            self.class_counts[label] += 1
            self.token_counts[label].update(tokens)
            self.vocabulary.update(tokens)
        n = sum(self.class_counts.values())
        self.log_prior = {
            label: math.log((self.class_counts[label] + 1) / (n + len(self.labels)))
            for label in self.labels}
        self.log_denominator = {
            label: math.log(sum(self.token_counts[label].values()) + max(1, len(self.vocabulary)))
            for label in self.labels}

    def predict(self, text):
        counts = Counter(token for token in words(text) if token in self.vocabulary)
        scores = {}
        for label in self.labels:
            scores[label] = self.log_prior[label] + sum(
                count * (math.log(self.token_counts[label][token] + 1) - self.log_denominator[label])
                for token, count in sorted(counts.items()))
        # Explicit stable category order breaks exact score ties.
        return max(self.labels, key=lambda label: scores[label])


def score_predictions(labels, predictions, categories=CATEGORIES):
    matrix = {gold: {pred: 0 for pred in categories} for gold in categories}
    for gold, predicted in zip(labels, predictions):
        matrix[gold][predicted] += 1
    correct = sum(matrix[label][label] for label in categories)
    per_class = {}
    for label in categories:
        tp = matrix[label][label]
        support = sum(matrix[label].values())
        predicted = sum(matrix[gold][label] for gold in categories)
        per_class[label] = {
            "support": support, "predicted": predicted, "correct": tp,
            "precision": ratio(tp, predicted), "recall": ratio(tp, support),
            "f1": ratio(2 * tp, support + predicted),
        }
    return {"count": len(labels), "correct": correct,
            "accuracy": ratio(correct, len(labels)), "per_class": per_class,
            "confusion_matrix_gold_rows_prediction_columns": matrix}


def classifier_audit(split_episodes):
    rows = {split: [(last_user(event), event["gold"]["category"])
                    for _, event in events(episodes)]
            for split, episodes in split_episodes.items()}
    model = NaiveBayes(rows["train"])
    majority = max(CATEGORIES, key=lambda cat: model.class_counts[cat])
    binary_labels = ("write", "no_write")
    binary_train_counts = Counter("write" if label in WRITE_CATEGORIES else "no_write"
                                  for _, label in rows["train"])
    binary_majority = max(binary_labels, key=lambda label: binary_train_counts[label])
    evaluations = {}
    for split in ("dev", "test"):
        actual = [label for _, label in rows[split]]
        predicted = [model.predict(text) for text, _ in rows[split]]
        result = score_predictions(actual, predicted)
        result["subsets"] = prediction_subsets(split_episodes[split], actual, predicted)
        result["majority_baseline"] = {
            "train_selected_label": majority,
            **score_predictions(actual, [majority] * len(actual))}
        actual_binary = ["write" if label in WRITE_CATEGORIES else "no_write" for label in actual]
        pred_binary = ["write" if label in WRITE_CATEGORIES else "no_write" for label in predicted]
        result["binary_from_six_class_predictions"] = score_predictions(actual_binary, pred_binary, binary_labels)
        result["binary_majority_baseline"] = {
            "train_selected_label": binary_majority,
            **score_predictions(actual_binary, [binary_majority] * len(actual), binary_labels)}
        evaluations[split] = result
    return {
        "model": "multinomial_naive_bayes", "features": "word counts in final user message only",
        "fit_split": "train", "hyperparameters": {"token_alpha": 1, "class_prior_alpha": 1},
        "unknown_heldout_tokens": "ignored; vocabulary fitted on train only",
        "label_order_for_ties": list(CATEGORIES), "seed": "not used; deterministic",
        "train_count": len(rows["train"]), "train_class_counts": complete(model.class_counts, CATEGORIES),
        "train_vocabulary_size": len(model.vocabulary), "evaluation": evaluations,
        "interpretation": "A lexical shortcut diagnostic, not an end-to-end memory-policy evaluation. No dev/test fitting or tuning.",
    }



def active_exception_count(state, day, mode="date_active"):
    """Count actual pre-event exception records, never generated gold deltas.

    ISO dates are validated by validate.py; lexicographic comparison is exact
    for that representation. Persistent/open records are active until removed.
    Windows are active on both endpoints. The alternate stored_records mode
    also counts out-of-window records still present in the serialized state.
    """
    if mode not in ("date_active", "stored_records"):
        raise ValueError("unknown exception-count mode: " + str(mode))
    count = 0
    for attribute_state in state.values():
        for record in attribute_state.get("exceptions", {}).values():
            validity = record["validity"]
            if (mode == "stored_records" or validity["kind"] in ("persistent", "open")
                    or validity["from"] <= day <= validity["to"]):
                count += 1
    return count


def structural_rows(episodes, mode="date_active"):
    """List of ((1-based event ordinal, pre-event exception count), label)."""
    result = []
    for episode in episodes:
        before = episode["initial_state"]
        for ordinal, event in enumerate(episode["events"], 1):
            result.append(((ordinal, active_exception_count(before, event["date"], mode)),
                           event["gold"]["category"]))
            before = event["gold"]["state_after"]
    return result


def contrast_target_event_keys(episodes):
    """Find the differing event from paired dialogue, without label features."""
    groups = defaultdict(list)
    for episode in episodes:
        if episode.get("contrast_group") is not None:
            groups[episode["contrast_group"]].append(episode)
    keys = set()
    for pair in groups.values():
        if len(pair) != 2 or len(pair[0]["events"]) != len(pair[1]["events"]):
            continue
        differing = [i for i, (a, b) in enumerate(zip(pair[0]["events"], pair[1]["events"]))
                     if a["dialogue"] != b["dialogue"]]
        if len(differing) == 1:
            i = differing[0]
            keys.update((episode["episode_id"], episode["events"][i]["event_id"])
                        for episode in pair)
    return keys


def prediction_subsets(episodes, actual, predicted):
    targets = contrast_target_event_keys(episodes)
    flags = [(episode["episode_id"], event["event_id"]) in targets
             for episode, event in events(episodes)]
    return {
        name: score_predictions([label for label, flag in zip(actual, flags) if flag == wanted],
                                [label for label, flag in zip(predicted, flags) if flag == wanted])
        for name, wanted in (("contrast_focal_events", True), ("other_events", False))
    }


def structural_classifier_audit(split_episodes):
    """Train-only bucket-majority baselines for chronology/state shortcuts.

    Both interpretations use the identical train-fit rule, held-out event
    denominator, six categories, and fallback; neither consumes dialogue,
    attribute/value names, IDs, future state, or the current event's label.
    """
    result = {
        "model": "train_fitted_bucket_majority",
        "features": ["1-based event ordinal within episode", "pre-event exception count across all attributes"],
        "fit_split": "train", "label_order_for_ties": list(CATEGORIES),
        "fallback": "global train-majority category for a bucket absent from train",
        "date_active_definition": "Count persistent/open records plus window records with from <= event.date <= to, using initial_state or the immediately preceding state_after.",
        "stored_records_definition": "Count every actual exception record in the same pre-event state, including windows outside their date interval.",
        "interpretation": "The primary metric is date_active; stored_records is a separately named sensitivity check, not an alternative selected after evaluation.",
    }
    for mode in ("date_active", "stored_records"):
        rows = {split: structural_rows(episodes, mode) for split, episodes in split_episodes.items()}
        buckets = defaultdict(Counter)
        total = Counter()
        for feature, label in rows["train"]:
            buckets[feature][label] += 1
            total[label] += 1
        fallback = max(CATEGORIES, key=lambda label: total[label])
        selected = {feature: max(CATEGORIES, key=lambda label: counts[label])
                    for feature, counts in buckets.items()}
        evaluations = {}
        for split in ("dev", "test"):
            actual = [label for _, label in rows[split]]
            predicted = [selected.get(feature, fallback) for feature, _ in rows[split]]
            unseen = sum(feature not in selected for feature, _ in rows[split])
            evaluations[split] = {
                **score_predictions(actual, predicted),
                "unseen_bucket_events": unseen,
                "unseen_bucket_event_fraction": ratio(unseen, len(actual)),
                "distinct_evaluation_buckets": len({feature for feature, _ in rows[split]}),
                "unseen_distinct_buckets": len({feature for feature, _ in rows[split] if feature not in selected}),
                "subsets": prediction_subsets(split_episodes[split], actual, predicted),
            }
        result[mode] = {
            "train_count": len(rows["train"]), "train_bucket_count": len(buckets),
            "train_class_counts": complete(total, CATEGORIES), "fallback_label": fallback,
            "train_buckets": [{"event_ordinal": feature[0], "exception_count": feature[1],
                               "train_class_counts": complete(buckets[feature], CATEGORIES),
                               "selected_label": selected[feature]}
                              for feature in sorted(buckets)],
            "evaluation": evaluations,
        }
    return result


def utterance_diversity_audit(episodes):
    """Exact normalized assistant diversity and explicit full-attribute rate."""
    utterances, raw_utterances = set(), set()
    assistant_count = event_count = full_attribute_events = 0
    assistant_present_events = assistant_no_question_events = 0
    by_category = {category: Counter() for category in CATEGORIES}
    examples = []
    for episode in episodes:
        names = [tuple(words(catalog["attribute"])) for catalog in episode["attributes"]]
        for event in episode["events"]:
            event_count += 1
            matched = False
            assistant_present = assistant_question_mark = False
            for message in event["dialogue"]:
                tokens = tuple(words(message["content"]))
                if message["role"] == "assistant":
                    assistant_count += 1
                    utterances.add(tokens)
                    raw_utterances.add(message["content"])
                    assistant_present = True
                    assistant_question_mark |= any(mark in message["content"]
                                                   for mark in ("?", "？", "﹖", "؟", "¿"))
                if not matched:
                    matched = any(name and any(tokens[i:i+len(name)] == name
                                              for i in range(len(tokens)-len(name)+1))
                                  for name in names)
            assistant_present_events += int(assistant_present)
            assistant_no_question_events += int(assistant_present and not assistant_question_mark)
            category = event["gold"]["category"]
            by_category[category]["events"] += 1
            by_category[category]["full_catalog_attribute_mention_events"] += int(matched)
            full_attribute_events += int(matched)
            if matched and len(examples) < 5:
                examples.append({"episode_id": episode["episode_id"], "event_id": event["event_id"]})
    return {
        "assistant_utterances": assistant_count,
        "unique_raw_assistant_utterances": len(raw_utterances),
        "unique_normalized_assistant_utterances": len(utterances),
        "assistant_unique_fraction": ratio(len(utterances), assistant_count),
        "assistant_present_events": assistant_present_events,
        "assistant_no_question_mark_events": assistant_no_question_events,
        "assistant_no_question_mark_event_fraction": ratio(assistant_no_question_events, assistant_present_events),
        "assistant_no_question_mark_fraction_of_all_events": ratio(assistant_no_question_events, event_count),
        "assistant_question_mark_definition": "Events containing at least one assistant message and none of ?, ？, ﹖, ؟, ¿ in any assistant message; primary fraction denominator is events containing an assistant, not all events. This punctuation diagnostic does not classify rhetorical or implicit questions.",
        "events": event_count,
        "full_catalog_attribute_mention_events": full_attribute_events,
        "full_catalog_attribute_mention_event_fraction": ratio(full_attribute_events, event_count),
        "full_attribute_match_definition": "Any full canonical attribute in this episode's catalog, as contiguous normalized tokens inside one dialogue message; no cross-message matches; event counted once.",
        "assistant_uniqueness_definition": "Distinct exact tuples of words() normalized tokens, punctuation-insensitive; no fuzzy or semantic matching.",
        "by_category": {category: {**dict(counts), "full_catalog_attribute_mention_event_fraction":
                                    ratio(counts["full_catalog_attribute_mention_events"], counts["events"])}
                        for category, counts in by_category.items()},
        "full_attribute_match_examples": examples,
    }


def episode_variability_audit(episodes):
    lengths = Counter(len(episode["events"]) for episode in episodes)
    attribute_counts = Counter(len(episode["attributes"]) for episode in episodes)
    category_counts = {category: Counter() for category in CATEGORIES}
    sequences = set()
    for episode in episodes:
        sequence = tuple(event["gold"]["category"] for event in episode["events"])
        sequences.add(sequence)
        counts = Counter(sequence)
        for category in CATEGORIES:
            category_counts[category][counts[category]] += 1
    n = len(episodes)
    mean = ratio(sum(size * count for size, count in lengths.items()), n)
    return {
        "episodes": n, "attributes_per_episode": sorted_counts(attribute_counts),
        "exactly_two_attribute_episodes": attribute_counts[2],
        "exactly_two_attribute_episode_fraction": ratio(attribute_counts[2], n),
        "events_per_episode": sorted_counts(lengths),
        "event_count_min": min(lengths) if lengths else None,
        "event_count_max": max(lengths) if lengths else None,
        "event_count_mean": mean,
        "event_count_population_stddev": math.sqrt(sum(count * (size - mean) ** 2
                                                        for size, count in lengths.items()) / n) if n else None,
        "distinct_category_sequences": len(sequences),
        "category_count_per_episode": {category: sorted_counts(counts)
                                       for category, counts in category_counts.items()},
    }


def class_exclusive_phrase_audit(episodes, surface="all_dialogue", min_n=1, max_n=8,
                                 threshold=0.15, example_limit=12):
    """Bounded report of class-exclusive recurring n-grams in a single split.

    Support counts EVENTS, once per phrase per event, across messages with no
    cross-message n-grams. A phrase is exclusive only when its event support is
    zero for every other category in the SAME split and selected surface.
    """
    if surface not in ("all_dialogue", "last_user"):
        raise ValueError("unknown phrase audit surface: " + str(surface))
    support = {}
    counts = Counter()
    category_index = {category: i for i, category in enumerate(CATEGORIES)}
    for _, event in events(episodes):
        category = event["gold"]["category"]
        counts[category] += 1
        index = category_index[category]
        messages = ([last_user(event)] if surface == "last_user"
                    else [message["content"] for message in event["dialogue"]])
        seen = set()
        for message in messages:
            tokens = words(message)
            for n in range(min_n, max_n + 1):
                seen.update(tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1))
        for phrase in seen:
            previous = support.get(phrase)
            if previous is None:
                support[phrase] = [index, 1]
            elif previous[0] == index:
                previous[1] += 1
            elif previous[0] != -1:
                # Other-category support disqualifies this phrase permanently;
                # its further counts are immaterial to this exclusive audit.
                previous[0] = -1
    by_category = {}
    for category, index in category_index.items():
        exclusive = [(phrase, count) for phrase, (owner, count) in support.items()
                     if owner == index and count >= 2]
        exclusive.sort(key=lambda item: (-item[1], len(item[0]), item[0]))
        violations = [(phrase, count) for phrase, count in exclusive
                      if count > threshold * counts[category]]
        by_length = {}
        for n in range(min_n, max_n + 1):
            of_length = [(phrase, count) for phrase, count in exclusive if len(phrase) == n]
            violations_n = [(phrase, count) for phrase, count in violations if len(phrase) == n]
            by_length[str(n)] = {
                "recurring_class_exclusive_phrases": len(of_length),
                "violations_count": len(violations_n),
                "max_event_support": max((count for _, count in of_length), default=0),
                "max_event_fraction": ratio(max((count for _, count in of_length), default=0), counts[category]),
            }
        def examples(rows):
            return [{"phrase": " ".join(phrase), "ngram_words": len(phrase),
                     "event_support": count, "category_events": counts[category],
                     "event_fraction": ratio(count, counts[category])}
                    for phrase, count in rows[:example_limit]]
        by_category[category] = {
            "events": counts[category],
            "recurring_class_exclusive_phrases": len(exclusive),
            "max_event_support": max((count for _, count in exclusive), default=0),
            "max_event_fraction": ratio(max((count for _, count in exclusive), default=0), counts[category]),
            "violations_count": len(violations), "violation_examples": examples(violations),
            "highest_frequency_examples": examples(exclusive), "by_ngram_length": by_length,
        }
    return {
        "surface": surface, "events": sum(counts.values()),
        "distinct_ngrams_examined": len(support), "by_category": by_category,
        "violations_count": sum(item["violations_count"] for item in by_category.values()),
        "all_categories_within_threshold": not any(item["violations_count"] for item in by_category.values()),
    }


def recurring_phrases_audit(split_episodes):
    return {
        "normalization": NORMALIZATION, "ngram_min_words": 1, "ngram_max_words": 8,
        "minimum_event_support_for_recurring": 2, "maximum_event_fraction": 0.15,
        "denominator": "All events of the phrase's sole category in the same split, not messages or token occurrences.",
        "exclusivity": "Nonzero event support in exactly one of the six categories within the same split and selected surface.",
        "comparison": "Counts each distinct phrase once per event, includes all dialogue roles, never crosses message boundaries; violation means strictly more than 15%.",
        "scope_limitations": "This detailed report covers 1 through 8 contiguous normalized words, including single words. The separate class_exclusive_long_phrases report checks all longer contiguous phrase lengths for threshold violations. Discontinuous templates and semantic equivalents are not covered; this is not a proof of shortcut freedom.",
        "examples_per_category_limit": 12,
        "by_split": {split: {surface: class_exclusive_phrase_audit(episodes, surface)
                             for surface in ("all_dialogue", "last_user")}
                     for split, episodes in split_episodes.items()},
    }



def class_exclusive_long_phrase_audit(episodes, threshold=0.15, example_limit=6):
    """Exact threshold-violation search for every contiguous phrase >=9 words.

    Apriori pruning is by category support, NOT category exclusivity. A long
    phrase exceeding a category's threshold has a prefix exceeding that same
    threshold. All occurrences of each candidate are counted in every class,
    even where its prefix is not frequent, before deciding exclusivity.
    """
    category_index = {category: index for index, category in enumerate(CATEGORIES)}
    rows = [(category_index[event["gold"]["category"]],
             [tuple(words(message["content"])) for message in event["dialogue"]])
            for _, event in events(episodes)]
    totals = Counter(index for index, _ in rows)
    max_words = max((len(tokens) for _, messages in rows for tokens in messages), default=0)
    # Frequent eight-word seeds need support by every class. The short-phrase
    # exclusive audit deliberately discards nonexclusive counts, so its map
    # cannot safely seed this exact longer-phrase search.
    seed = {}
    for index, messages in rows:
        seen = {tokens[i:i+8] for tokens in messages for i in range(len(tokens)-7)}
        for phrase in seen:
            counts = seed.setdefault(phrase, [0] * len(CATEGORIES))
            counts[index] += 1
    def frequent(counts):
        return any(count >= 2 and count > threshold * totals[index]
                   for index, count in enumerate(counts))
    prefixes = {phrase for phrase, counts in seed.items() if frequent(counts)}
    seed_count = len(seed)
    del seed
    summary = {category: {"events": totals[index], "violations_count": 0,
                          "max_violation_event_support": 0, "max_violation_event_fraction": 0.0,
                          "violation_examples": [], "violations_by_ngram_length": Counter()}
               for category, index in category_index.items()}
    top = {category: [] for category in CATEGORIES}
    levels = []
    n = 9
    while prefixes and n <= max_words:
        candidates = {}
        for index, messages in rows:
            seen = set()
            for tokens in messages:
                for i in range(len(tokens)-n+1):
                    if tokens[i:i+n-1] in prefixes:
                        seen.add(tokens[i:i+n])
            for phrase in seen:
                counts = candidates.setdefault(phrase, [0] * len(CATEGORIES))
                counts[index] += 1
        next_prefixes = set()
        level_violations = 0
        for phrase, counts in candidates.items():
            if not frequent(counts):
                continue
            next_prefixes.add(phrase)
            owners = [index for index, count in enumerate(counts) if count]
            if len(owners) != 1:
                continue
            index = owners[0]
            category, count = CATEGORIES[index], counts[index]
            record = summary[category]
            record["violations_count"] += 1
            record["violations_by_ngram_length"][n] += 1
            record["max_violation_event_support"] = max(record["max_violation_event_support"], count)
            record["max_violation_event_fraction"] = record["max_violation_event_support"] / totals[index]
            top[category].append((phrase, count))
            level_violations += 1
        for category in CATEGORIES:
            top[category] = sorted(top[category], key=lambda item: (-item[1], len(item[0]), item[0]))[:example_limit]
        levels.append({"ngram_words": n, "candidate_phrases": len(candidates),
                       "frequent_phrases": len(next_prefixes), "violations_count": level_violations})
        prefixes = next_prefixes
        n += 1
    for category in CATEGORIES:
        record = summary[category]
        record["violations_by_ngram_length"] = sorted_counts(record["violations_by_ngram_length"])
        record["violation_examples"] = [
            {"phrase": " ".join(phrase), "ngram_words": len(phrase), "event_support": count,
             "category_events": record["events"], "event_fraction": count / record["events"]}
            for phrase, count in top[category]]
    total_violations = sum(record["violations_count"] for record in summary.values())
    return {
        "events": len(rows), "ngram_min_words": 9, "maximum_message_words": max_words,
        "exhaustive_through_max_message_words": True,
        "seed_distinct_eight_word_phrases": seed_count,
        "expanded_lengths": levels,
        "stop_reason": "no frequent prefixes remain" if not prefixes else "reached maximum message length",
        "violations_count": total_violations,
        "max_violation_event_fraction": max((record["max_violation_event_fraction"]
                                              for record in summary.values()), default=0.0),
        "all_categories_within_threshold": total_violations == 0,
        "by_category": summary,
    }


def long_phrases_audit(split_episodes):
    return {
        "normalization": NORMALIZATION, "ngram_min_words": 9,
        "minimum_event_support_for_recurring": 2, "maximum_event_fraction": 0.15,
        "surface": "all_dialogue",
        "denominator": "All events of the phrase's sole category in the same split; each phrase counted at most once per event.",
        "exclusivity": "Nonzero event support in exactly one of the six categories within the same split, across all dialogue roles.",
        "algorithm": "Exact frequent-prefix Apriori: seed every 8-gram with support >=2 and >15% in any category; extend only frequent prefixes, count every candidate in all six categories, and stop at maximum message length or when no frequent prefixes remain. Prefixes need not be class-exclusive.",
        "completeness": "A >=9-word phrase with support >=2 and >15% in a class must have a prefix with at least that support, so no threshold-violating contiguous phrase can be pruned. Combined with the detailed 1-8-word report, this covers every length present in the corpus, without crossing messages.",
        "output_limitations": "Reports exact violation counts and the maximum violating fraction, not the maximum fraction among below-threshold phrases. Zero maximum means no violation, not that no longer class-exclusive phrase exists. Does not cover discontinuous or semantic-equivalence templates.",
        "examples_per_category_limit": 6,
        "by_split": {split: class_exclusive_long_phrase_audit(episodes)
                     for split, episodes in split_episodes.items()},
    }


def phrase_occurrences(tokens, needle):
    n = len(needle)
    return sum(tuple(tokens[i:i+n]) == needle for i in range(len(tokens) - n + 1))


def keyword_audit(episodes):
    result = {}
    for bucket in ("write", "no_write"):
        relevant = [event for _, event in events(episodes)
                    if (event["gold"]["category"] in WRITE_CATEGORIES) == (bucket == "write")]
        result[bucket] = {"events": len(relevant), "keywords": {}}
        for keyword in KEYWORDS:
            needle = tuple(words(keyword))
            event_hits = occurrence_total = user_total = last_total = 0
            last_hits = user_hits = 0
            for event in relevant:
                counts = [(message["role"], phrase_occurrences(words(message["content"]), needle))
                          for message in event["dialogue"]]
                total = sum(count for _, count in counts)
                users = sum(count for role, count in counts if role == "user")
                last = phrase_occurrences(words(last_user(event)), needle)
                occurrence_total += total
                user_total += users
                last_total += last
                event_hits += bool(total)
                user_hits += bool(users)
                last_hits += bool(last)
            result[bucket]["keywords"][keyword] = {
                "all_dialogue_occurrences": occurrence_total, "all_dialogue_event_hits": event_hits,
                "user_message_occurrences": user_total, "user_message_event_hits": user_hits,
                "last_user_occurrences": last_total, "last_user_event_hits": last_hits,
            }
    result["present_in_both_buckets"] = {
        keyword: all(result[bucket]["keywords"][keyword]["all_dialogue_occurrences"] > 0
                     for bucket in ("write", "no_write")) for keyword in KEYWORDS}
    return result


def transition_signature(episode, index):
    event = episode["events"][index]
    before = episode["initial_state"] if index == 0 else episode["events"][index-1]["gold"]["state_after"]
    after = event["gold"]["state_after"]
    changes = []
    for attribute in sorted(set(before) | set(after)):
        a, b = before.get(attribute, {}), after.get(attribute, {})
        if a.get("general") != b.get("general"):
            changes.append([attribute, "general", a.get("general"), b.get("general")])
        ae, be = a.get("exceptions", {}), b.get("exceptions", {})
        for scope in sorted(set(ae) | set(be)):
            if ae.get(scope) != be.get(scope):
                changes.append([attribute, scope, ae.get(scope), be.get(scope)])
    return canonical({"decision": event["gold"]["decision"], "changes": changes})


def suffix_feature(event, k):
    return tuple((message["role"], message["content"]) for message in event["dialogue"][-k:])


def ceiling(rows):
    buckets = defaultdict(Counter)
    for feature, label in rows:
        buckets[feature][label] += 1
    correct = sum(max(counts.values()) for counts in buckets.values())
    return {"examples": len(rows), "distinct_inputs": len(buckets), "maximum_correct": correct,
            "accuracy_ceiling": ratio(correct, len(rows))}


def contrast_audit(episodes):
    grouped = defaultdict(list)
    for episode in episodes:
        if episode.get("contrast_group") is not None:
            grouped[episode["contrast_group"]].append(episode)
    targets, invalid = [], []
    for group in sorted(grouped):
        pair = grouped[group]
        if len(pair) != 2 or len(pair[0]["events"]) != len(pair[1]["events"]):
            invalid.append({"contrast_group": group, "reason": "not two equal-length episodes"})
            continue
        differences = []
        for i, (a, b) in enumerate(zip(pair[0]["events"], pair[1]["events"])):
            if len(a["dialogue"]) != len(b["dialogue"]):
                differences.append((i, None))
            else:
                differences.extend((i, j) for j, (ma, mb) in enumerate(zip(a["dialogue"], b["dialogue"]))
                                   if (ma["role"], ma["content"]) != (mb["role"], mb["content"]))
        if len(differences) != 1 or differences[0][1] is None:
            invalid.append({"contrast_group": group, "reason": "not exactly one differing message"})
            continue
        event_i, message_i = differences[0]
        ea, eb = pair[0]["events"][event_i], pair[1]["events"][event_i]
        if ea["dialogue"][message_i]["role"] != "user" or eb["dialogue"][message_i]["role"] != "user":
            invalid.append({"contrast_group": group, "reason": "differing message is not user"})
            continue
        transitions = [transition_signature(ep, event_i) for ep in pair]
        targets.append((group, pair, event_i, message_i, transitions))
    by_k = {}
    for k in range(1, 9):
        all_category, all_transition, tied_category, tied_transition = [], [], [], []
        tied_pairs = different_category_pairs = different_transition_pairs = 0
        for _, pair, event_i, _, transitions in targets:
            es = [ep["events"][event_i] for ep in pair]
            features = [suffix_feature(event, k) for event in es]
            cat_rows = [(feature, event["gold"]["category"]) for feature, event in zip(features, es)]
            tr_rows = list(zip(features, transitions))
            all_category.extend(cat_rows)
            all_transition.extend(tr_rows)
            if features[0] == features[1]:
                tied_pairs += 1
                different_category_pairs += es[0]["gold"]["category"] != es[1]["gold"]["category"]
                different_transition_pairs += transitions[0] != transitions[1]
                tied_category.extend(cat_rows)
                tied_transition.extend(tr_rows)
        by_k[str(k)] = {
            "target_pairs": len(targets), "tied_pairs": tied_pairs,
            "untied_pairs": len(targets) - tied_pairs,
            "tied_pairs_with_different_categories": different_category_pairs,
            "tied_pairs_with_different_transitions": different_transition_pairs,
            "tied_category": ceiling(tied_category), "tied_transition": ceiling(tied_transition),
            "all_target_category": ceiling(all_category), "all_target_transition": ceiling(all_transition),
        }
    examples = []
    for group, pair, event_i, message_i, transitions in targets[:5]:
        examples.append({
            "contrast_group": group, "episode_ids": [ep["episode_id"] for ep in pair],
            "target_event_index": event_i + 1, "differing_message_index": message_i + 1,
            "common_suffix_messages": len(pair[0]["events"][event_i]["dialogue"]) - message_i - 1,
            "categories": [ep["events"][event_i]["gold"]["category"] for ep in pair],
            "different_semantic_transitions": transitions[0] != transitions[1],
        })
    return {"contrast_groups": len(grouped), "target_pairs": len(targets),
            "invalid_groups": invalid, "by_k": by_k, "examples": examples}


def message_records(episodes):
    for episode, event in events(episodes):
        for index, message in enumerate(event["dialogue"], 1):
            yield {"episode_id": episode["episode_id"], "event_id": event["event_id"],
                   "message_index": index, "text": message["content"]}


def longest_common_ngram(train_episodes, test_episodes):
    """Exact longest common contiguous token sequence, never across turns.

    A suffix automaton indexes deduplicated train turns separated by an integer
    token not used by any word. Matching test words can never cross that token.
    Runtime and index size are linear in the indexed/queried token counts.
    """
    train = []
    train_seen = set()
    for record in message_records(train_episodes):
        tokens = tuple(words(record["text"]))
        if tokens and tokens not in train_seen:
            train_seen.add(tokens)
            train.append((record, tokens))
    vocabulary = {}
    transitions, links, lengths, first_message, first_offset = [{}], [-1], [0], [-1], [-1]
    last = 0

    def extend(token, message_i, word_i):
        nonlocal last
        current = len(transitions)
        transitions.append({})
        lengths.append(lengths[last] + 1)
        links.append(0)
        first_message.append(message_i)
        first_offset.append(word_i)
        p = last
        while p >= 0 and token not in transitions[p]:
            transitions[p][token] = current
            p = links[p]
        if p >= 0:
            q = transitions[p][token]
            if lengths[p] + 1 == lengths[q]:
                links[current] = q
            else:
                clone = len(transitions)
                transitions.append(transitions[q].copy())
                lengths.append(lengths[p] + 1)
                links.append(links[q])
                first_message.append(first_message[q])
                first_offset.append(first_offset[q])
                while p >= 0 and transitions[p].get(token) == q:
                    transitions[p][token] = clone
                    p = links[p]
                links[q] = links[current] = clone
        last = current

    for message_i, (_, tokens) in enumerate(train):
        for word_i, word in enumerate(tokens):
            if word not in vocabulary:
                vocabulary[word] = len(vocabulary) + 1
            extend(vocabulary[word], message_i, word_i)
        extend(0, -1, -1)
    best, best_phrase, train_example, test_example = 0, "", None, None
    test_seen = set()
    for record in message_records(test_episodes):
        tokens = tuple(words(record["text"]))
        if tokens in test_seen:
            continue
        test_seen.add(tokens)
        state = length = 0
        for offset, word in enumerate(tokens):
            token = vocabulary.get(word, -1)
            while state and token not in transitions[state]:
                state = links[state]
                length = lengths[state]
            if token in transitions[state]:
                state = transitions[state][token]
                length += 1
            else:
                state = length = 0
            if length > best:
                best = length
                best_phrase = " ".join(tokens[offset - length + 1:offset + 1])
                train_record, train_words = train[first_message[state]]
                start = first_offset[state] - length + 1
                assert start >= 0 and tuple(train_words[start:start+length]) == tokens[offset-length+1:offset+1]
                train_example = {**train_record, "word_start": start}
                test_example = {**record, "word_start": offset - length + 1}
    return {
        "length_words": best, "phrase": best_phrase,
        "train_example": train_example, "test_example": test_example,
        "train_unique_normalized_messages": len(train),
        "test_unique_normalized_messages": len(test_seen),
        "algorithm": "exact suffix automaton over deduplicated train messages, separated by nonword sentinel",
        "tie_break": "first match in test episode/event/message/word order; first indexed train occurrence",
        "comparison_unit": "one dialogue message; no cross-message n-grams",
    }


def normalized_dialogue(dialogue):
    return tuple((message.get("role", ""), tuple(words(message["content"]))) for message in dialogue)


def extract_old_dialogues(value):
    """Find common legacy dialogue containers without interpreting gold text."""
    if isinstance(value, dict):
        for key, child in value.items():
            if key in ("dialogue", "conversation", "messages", "turns", "utterances") and isinstance(child, list):
                if child and all(isinstance(message, dict) and isinstance(message.get("content"), str)
                                 for message in child):
                    yield normalized_dialogue(child)
                    continue
                if child and all(isinstance(message, str) for message in child):
                    yield normalized_dialogue([{"role": "user" if i % 2 == 0 else "assistant", "content": text}
                                               for i, text in enumerate(child)])
                    continue
            if key not in ("gold", "rationale", "memory", "state_after", "initial_state"):
                yield from extract_old_dialogues(child)
    elif isinstance(value, list):
        for child in value:
            yield from extract_old_dialogues(child)


def old_overlap(split_episodes, paths):
    paths = [Path(path) for path in paths]
    if not paths:
        return {"status": "not_supplied", "sources": [],
                "note": "No old-corpus paths supplied. This does not establish old-data exclusion."}
    files = sorted({file for path in paths for file in
                    (path.rglob("*") if path.is_dir() else [path])
                    if file.is_file() and file.suffix.lower() in (".json", ".jsonl")}, key=str)
    old = set()
    sources = []
    for path in files:
        raw = path.read_bytes()
        payload = read_jsonl(path) if path.suffix.lower() == ".jsonl" else json.loads(raw)
        dialogues = list(extract_old_dialogues(payload))
        old.update(dialogues)
        sources.append({"file": path.name, "sha256": hashlib.sha256(raw).hexdigest(),
                        "dialogues_extracted": len(dialogues)})
    result = {}
    for split, episodes in split_episodes.items():
        hits = []
        for episode, event in events(episodes):
            if normalized_dialogue(event["dialogue"]) in old:
                hits.append({"episode_id": episode["episode_id"], "event_id": event["event_id"]})
        result[split] = {"overlapping_events": len(hits), "examples": hits[:10]}
    return {"status": "checked", "sources": sources, "unique_old_dialogues": len(old),
            "by_split": result, "comparison": "exact sequence of roles and normalized words per message",
            "limitation": "Checks exact whole-dialogue overlap, not paraphrases, domains, phrase reuse, or semantic similarity."}


def audit(root: Path, old_corpora=()):
    """Return a JSON-serializable deterministic report; do not write files.

    root contains train.jsonl, dev.jsonl and test.jsonl. Optional old_corpora
    accepts JSON/JSONL files or directories to inspect for dialogue overlap.
    """
    from build import legacy_overlap

    root = Path(root)
    split_episodes = {split: read_jsonl(root / (split + ".jsonl")) for split in SPLITS}
    all_episodes = [episode for split in SPLITS for episode in split_episodes[split]]
    return {
        "schema_version": 1, "normalization": NORMALIZATION,
        "data_sha256": {split: hashlib.sha256((root / (split + ".jsonl")).read_bytes()).hexdigest()
                        for split in SPLITS},
        "counts": {**{split: dataset_counts(episodes) for split, episodes in split_episodes.items()},
                   "overall": dataset_counts(all_episodes)},
        "last_user_bow": classifier_audit(split_episodes),
        "position_active_exception_majority": structural_classifier_audit(split_episodes),
        "utterance_diversity": {
            **{split: utterance_diversity_audit(episodes) for split, episodes in split_episodes.items()},
            "overall": utterance_diversity_audit(all_episodes)},
        "episode_variability": {
            **{split: episode_variability_audit(episodes) for split, episodes in split_episodes.items()},
            "overall": episode_variability_audit(all_episodes)},
        "class_exclusive_recurring_phrases": recurring_phrases_audit(split_episodes),
        "class_exclusive_long_phrases": long_phrases_audit(split_episodes),
        "keyword_occurrences": {
            **{split: keyword_audit(episodes) for split, episodes in split_episodes.items()},
            "overall": keyword_audit(all_episodes)},
        "contrast_suffix": {
            "features": "exact raw (role, content) pairs in final k messages of the differing event; no IDs, gold, memory, dates, or probes",
            "label_definition": "category: six protocol classes; transition: decision plus exact semantic state delta, not unchanged state",
            "ceiling_definition": "For each identical suffix input, take the most frequent gold label, then sum. Labels are used only to score, never as input.",
            "interpretation": "Tied subsets are the applicable suffix-only contrast test. Longer k may include the differing message; those pairs are reported as untied. Global collisions can lower the ceiling below 1/2.",
            "by_split": {split: contrast_audit(episodes) for split, episodes in split_episodes.items()}},
        "train_test_longest_common_ngram": longest_common_ngram(split_episodes["train"], split_episodes["test"]),
        "old_corpus_dialogue_overlap": old_overlap(split_episodes, old_corpora),
        "legacy_exact_checks": legacy_overlap(split_episodes),
        "limitations": [
            "Synthetic-data statistics do not certify naturalness, label semantics, or real-world generalization.",
            "The last-user probe measures six-category lexical predictability, not operation or downstream QA quality.",
            "A 1/2 tied-suffix ceiling applies to omitted-context inputs, not models that can read the earlier message or memory.",
            "Longest n-gram is exact lexical overlap only; split isolation and semantic validation are separate checks.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path(__file__).resolve().parent / "data")
    parser.add_argument("--old-corpus", action="append", default=[], type=Path,
                        help="Optional legacy JSON/JSONL path or directory; repeatable")
    args = parser.parse_args()
    report = audit(args.data_dir, old_corpora=args.old_corpus)
    path = args.data_dir / "audit.json"
    path.write_text(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print("Wrote " + str(path))


if __name__ == "__main__":
    main()
