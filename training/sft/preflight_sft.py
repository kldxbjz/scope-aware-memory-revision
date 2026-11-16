"""Real-tokenizer SFT preflight for both arms: lengths, TRL SFTTrainer preprocessing and collator masking.

Records two separate verdicts: the collator check and the SFTTrainer preprocessing check.
Usage: python preflight_sft.py --model DIR --sft-dir DIR --out report.json [--max-length 4096]
"""
import argparse
import json
import sys
from pathlib import Path

import torch
import transformers
import trl
import peft
from datasets import Dataset
from peft import LoraConfig
from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import SFTConfig, SFTTrainer

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sft_common import length_report, load_rows, to_example  # noqa: E402


def check_arm(arm, args, tokenizer, model):
    rows = load_rows(Path(args.sft_dir) / f"train_{arm}_sft.jsonl") + load_rows(Path(args.sft_dir) / f"dev_{arm}_sft.jsonl")
    lengths = length_report(tokenizer, rows, args.max_length)
    report = {"lengths": lengths}
    if lengths["over_max_length"]:
        report["verdict"] = "FAIL_OVERLENGTH"
        return report
    longest = sorted(rows, key=lambda r: len(r["prompt"]) + len(r["completion"]))[-3:]
    sample = longest + rows[:13]
    dataset = Dataset.from_list([to_example(r) for r in sample])
    config = SFTConfig(output_dir=str(Path(args.out).parent / f"preflight_{arm}"), max_length=args.max_length,
                       completion_only_loss=True, packing=False, per_device_train_batch_size=2, report_to="none",
                       bf16=True, max_steps=1)
    trainer = SFTTrainer(model=model, args=config, train_dataset=dataset, processing_class=tokenizer)
    processed = trainer.train_dataset
    report["processed_columns"] = processed.column_names
    problems = []
    end_ids = set(tokenizer.convert_tokens_to_ids(["<|im_end|>"])) | {tokenizer.eos_token_id}
    for i, (row, item) in enumerate(zip(sample, processed)):
        ids, mask = item["input_ids"], item.get("completion_mask")
        if mask is None:
            problems.append("no completion_mask column")
            break
        full = tokenizer.apply_chat_template(to_example(row)["prompt"] + to_example(row)["completion"], tokenize=True)
        supervised = [t for t, m in zip(ids, mask) if m]
        text = tokenizer.decode(supervised)
        if len(ids) < len(full) - 1:
            problems.append(f"row {i}: truncated ({len(ids)} < {len(full)})")
        if row["completion"] not in text:
            problems.append(f"row {i}: supervised span does not contain the completion")
        if not any(t in end_ids for t in supervised[-3:]):
            problems.append(f"row {i}: end-of-turn token not supervised")
        prompt_part = tokenizer.decode([t for t, m in zip(ids, mask) if not m])
        if row["completion"] in prompt_part:
            problems.append(f"row {i}: completion leaks into the unsupervised prompt part")
    report["sfttrainer_preprocessing"] = "PASS" if not problems else "FAIL"
    report["preprocessing_problems"] = problems[:10]
    batch = trainer.data_collator([processed[0], processed[len(sample) - 1], processed[3]])
    labels, attention = batch["labels"], batch.get("attention_mask")
    collator_problems = []
    for b, idx in enumerate([0, len(sample) - 1, 3]):
        item = processed[idx]
        n = len(item["input_ids"])
        expected = [t if m else -100 for t, m in zip(item["input_ids"], item["completion_mask"])]
        got = labels[b].tolist()
        if got[:n] != expected:
            collator_problems.append(f"batch row {b}: labels differ from completion mask")
        if any(x != -100 for x in got[n:]):
            collator_problems.append(f"batch row {b}: padding has loss")
        if attention is not None and attention[b].tolist()[n:] and any(attention[b].tolist()[n:]):
            collator_problems.append(f"batch row {b}: padding attended")
    report["collator"] = "PASS" if not collator_problems else "FAIL"
    report["collator_problems"] = collator_problems
    report["rendered_example_tail"] = tokenizer.decode(processed[0]["input_ids"])[-400:]
    report["verdict"] = "PASS" if report["collator"] == "PASS" and report["sfttrainer_preprocessing"] == "PASS" else "FAIL"
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--sft-dir", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--max-length", type=int, default=4096)
    args = parser.parse_args()
    tokenizer = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForCausalLM.from_pretrained(args.model, torch_dtype=torch.bfloat16)
    report = {"versions": {"torch": torch.__version__, "transformers": transformers.__version__, "trl": trl.__version__,
                           "peft": peft.__version__},
              "eos_token": tokenizer.eos_token, "pad_token": tokenizer.pad_token,
              "arms": {arm: check_arm(arm, args, tokenizer, model) for arm in ("scope", "crud")}}
    report["verdict"] = "PASS" if all(a["verdict"] == "PASS" for a in report["arms"].values()) else "FAIL"
    Path(args.out).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verdict": report["verdict"], **{a: {k: v for k, v in r.items() if k in ("verdict", "lengths", "collator", "sfttrainer_preprocessing")}
                                                         for a, r in report["arms"].items()}}, indent=1))
    sys.exit(0 if report["verdict"] == "PASS" else 1)


if __name__ == "__main__":
    main()
