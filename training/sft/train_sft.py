"""LoRA SFT of one arm on protocol-v1 rows with TRL; resumes from the last checkpoint after preemption.

Usage: python train_sft.py --model DIR --sft-dir DIR --arm scope --output-dir DIR [--max-steps N | --epochs E]
train_summary.json records the arm and the SHA-256 of the policy instruction in the rows; baseline.py checks both
before it evaluates the adapter.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

import torch
from datasets import Dataset
from peft import LoraConfig
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.trainer_utils import get_last_checkpoint
from trl import SFTConfig, SFTTrainer

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sft_common import length_report, load_rows, to_example  # noqa: E402


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", required=True)
    p.add_argument("--sft-dir", required=True)
    p.add_argument("--arm", choices=("scope", "crud"), required=True)
    p.add_argument("--output-dir", required=True)
    p.add_argument("--max-length", type=int, default=4096)
    p.add_argument("--epochs", type=float, default=2.0)
    p.add_argument("--max-steps", type=int, default=-1)
    p.add_argument("--lr", type=float, default=1e-4)
    p.add_argument("--lora-r", type=int, default=16)
    p.add_argument("--lora-alpha", type=int, default=32)
    p.add_argument("--batch-size", type=int, default=4)
    p.add_argument("--grad-accum", type=int, default=4)
    p.add_argument("--seed", type=int, default=0)
    args = p.parse_args()
    out = Path(args.output_dir)
    if (out / "DONE").exists():
        print(f"{out} already finished")
        return
    out.mkdir(parents=True, exist_ok=True)
    tokenizer = AutoTokenizer.from_pretrained(args.model)
    rows = load_rows(Path(args.sft_dir) / f"train_{args.arm}_sft.jsonl")
    instructions = {r["system"] for r in rows}
    if len(instructions) != 1 or any(r["arm"] != args.arm for r in rows):
        sys.exit(f"rows must all be {args.arm} rows with one policy instruction")
    instruction_sha = hashlib.sha256(instructions.pop().encode("utf-8")).hexdigest()
    lengths = length_report(tokenizer, rows, args.max_length)
    if lengths["over_max_length"]:
        sys.exit(f"refusing to truncate: {lengths}")
    model = AutoModelForCausalLM.from_pretrained(args.model, torch_dtype=torch.bfloat16)
    model.config.use_cache = False
    config = SFTConfig(
        output_dir=str(out), num_train_epochs=args.epochs, max_steps=args.max_steps, learning_rate=args.lr,
        per_device_train_batch_size=args.batch_size, gradient_accumulation_steps=args.grad_accum,
        lr_scheduler_type="cosine", warmup_ratio=0.03, bf16=True, gradient_checkpointing=True,
        gradient_checkpointing_kwargs={"use_reentrant": False}, logging_steps=5, save_strategy="steps",
        save_steps=50, save_total_limit=2, report_to="none", seed=args.seed, max_length=args.max_length,
        completion_only_loss=True, packing=False)
    trainer = SFTTrainer(model=model, args=config, train_dataset=Dataset.from_list([to_example(r) for r in rows]),
                         processing_class=tokenizer,
                         peft_config=LoraConfig(r=args.lora_r, lora_alpha=args.lora_alpha, lora_dropout=0.05,
                                                target_modules="all-linear", task_type="CAUSAL_LM"))
    trainer.train(resume_from_checkpoint=get_last_checkpoint(str(out)))
    trainer.save_model(str(out / "adapter"))
    tokenizer.save_pretrained(str(out / "adapter"))
    summary = {"arm": args.arm, "rows": len(rows), "policy_instruction_sha256": instruction_sha, "lengths": lengths,
               "args": vars(args),
               "log_history": trainer.state.log_history}
    (out / "train_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    (out / "DONE").write_text("ok\n", encoding="utf-8")
    losses = [h["loss"] for h in trainer.state.log_history if "loss" in h]
    print(json.dumps({"arm": args.arm, "steps": trainer.state.global_step, "first_loss": losses[:1],
                      "last_loss": losses[-1:], "lengths": lengths}))


if __name__ == "__main__":
    main()
