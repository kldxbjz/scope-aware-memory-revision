"""Oracle/rule plumbing smoke test; NOT SFT or learned-method evidence."""
import json
from .paths import FIXTURES

class Memory:
    def __init__(self, scoped):
        self.scoped, self.records, self.time = scoped, {}, -1

    def apply(self, event):
        if event["time"] <= self.time:
            raise ValueError("Events must be strictly chronological")
        self.time = event["time"]
        # Structured annotations are supplied by the toy oracle, not inferred.
        scope = event["scope"] if self.scoped else "*"
        key = (event["attribute"], scope)
        action = event["action"]
        if action in ("add", "update"):
            self.records[key] = event["value"]
        elif action == "delete":
            self.records.pop(key, None)
        elif action != "noop":
            raise ValueError("Unknown action")

    def answer(self, attribute, scope="*"):
        return self.records.get((attribute, scope), self.records.get((attribute, "*")))

def replay(episode, scoped):
    memory = Memory(scoped)
    correct = total = false_overwrites = opportunities = 0
    trace = []
    for event in episode["events"]:
        prior = memory.answer(event["attribute"])
        memory.apply({k: v for k, v in event.items() if k not in ("probes",)})
        if event["scope"] != "*" and prior is not None:
            opportunities += 1
            false_overwrites += memory.answer(event["attribute"]) != prior
        for probe in event["probes"]:
            predicted = memory.answer(probe["attribute"], probe["scope"])
            total += 1
            correct += predicted == probe["expected"]
            trace.append({"time": event["time"], "scope": probe["scope"],
                          "prediction": predicted, "expected": probe["expected"]})
    return {"qa_correct": correct, "qa_total": total,
            "qa_accuracy": correct / total if total else None,
            "false_overwrites": false_overwrites,
            "overwrite_opportunities": opportunities,
            "false_overwrite_rate": false_overwrites / opportunities if opportunities else None,
            "trace": trace}

def main():
    episode = json.loads((FIXTURES / "toy_episode.json").read_text())
    print(json.dumps({"evidence": "toy oracle engineering sanity only",
                      "scope_blind_rule": replay(episode, False),
                      "scope_aware_oracle": replay(episode, True)}, indent=2))

if __name__ == "__main__":
    main()
