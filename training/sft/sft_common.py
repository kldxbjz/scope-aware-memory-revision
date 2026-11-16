"""Shared helpers for protocol-v1 SFT: load exported rows, build chat examples, check lengths."""
import json
from pathlib import Path


def load_rows(path, limit=None):
    rows = [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
    return rows[:limit] if limit else rows


def to_example(row):
    """TRL conversational prompt-completion example; only system, prompt and completion are used."""
    return {"prompt": [{"role": "system", "content": row["system"]}, {"role": "user", "content": row["prompt"]}],
            "completion": [{"role": "assistant", "content": row["completion"]}]}


def full_length(tokenizer, example):
    ids = tokenizer.apply_chat_template(example["prompt"] + example["completion"], tokenize=True)
    return len(ids)


def length_report(tokenizer, rows, max_length):
    lengths = sorted(full_length(tokenizer, to_example(r)) for r in rows)
    over = sum(n > max_length for n in lengths)
    return {"n": len(lengths), "max": lengths[-1], "p50": lengths[len(lengths) // 2],
            "p99": lengths[int(0.99 * (len(lengths) - 1))], "over_max_length": over, "max_length": max_length}
