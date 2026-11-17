# Data generation prompt for Codex (protocol v1)

How `training/scope_revision_v1/` was produced: Codex could not run on the local machine, so GPT generated the data in a cloud copy of a snapshot of commit `eee84cb` (the repository files plus a short note on what to write and return), following the instructions below; their local paths refer to the original setup. The first release (v1) passed every contract check but had strong shortcuts. The feedback at the end produced v1.1, the release committed here, which was checked again with `replay_gold` and an independent audit.

---

你在 Windows 目录 `C:\Users\wzczs\Documents\Codex\scope-aware-memory-revision-codex` 里工作。它是 Scope-Aware Memory Revision 仓库的一份快照（没有 .git），你的产出之后会被复制回真正的仓库，重新检查后再提交。任务：按 `docs\protocol.md`（数据契约，一切以它为准）生成一套大规模、按时间顺序的合成数据 v1，供两组 SFT（通用 CRUD vs 场景感知）训练和评测使用。

先读：`README.md`、`docs\protocol.md`、`docs\sft-plan.md`、`docs\training-intake.md`、`fixtures\protocol_episode.json`（一个完整的示例 episode）。`training\scope_revision_training\`（v0.1）只用来了解旧格式和它的问题，不能复制其中任何对话、领域或措辞。

## 边界
- 只在 `training\scope_revision_v1\` 下新建文件，不改快照里任何其他文件。
- 不要初始化 git，不要提交或推送任何东西。
- 只用 Python 3 标准库：在 PowerShell 里于快照根目录用 `python` 运行。不联网、不装包、不调用任何模型或付费 API、不用 GPU。
- 所有生成的文本文件用 UTF-8，换行符一律是 LF（`open(path, "w", encoding="utf-8", newline="\n")`），因为它们会进 Linux 仓库；manifest 里的 SHA-256 按这些字节计算。

## 产出
```
training\scope_revision_v1\
  README.md       数据说明：生成方式、规模、类别分布、划分隔离、已知局限
  build.py        确定性生成器：python training\scope_revision_v1\build.py --seed 0 逐字节可复现
  banks\          按划分分开、手写的措辞库和场景库（train\ dev\ test\ 互不共享）
  validate.py     下面所有检查，任一失败就非零退出
  audit.py        统计和捷径探针，写 data\audit.json
  data\train.jsonl, data\dev.jsonl, data\test.jsonl   每行一个 episode，格式见 protocol §1
  data\manifest.json   每个文件的 SHA-256、条数、类别分布
  samples.md      每个划分随机 10 个 episode 的可读版本，供人工抽查
```
SFT 行和两组的标准输出不用你生成：它们由 `scope_memory\protocol.py` 按 protocol §6 从相邻的 gold 状态投影出来。你只需要给出对话、每个事件之后的 gold 状态、类别、决策和探针。

## 规模（下限）
- train 600 个 episode，dev 120，test 200；每个 episode 4–8 个事件，其中 2–4 个事件之后有 QA 探针。
- protocol §3 的六个类别在每个划分都要出现；test 里每类至少 80 个事件；按 QA 大类，test 里每类至少 60 个探针；四种探针类型（target / default / neighbor / boundary）都要有。
- 三种 validity（persistent / window / open）都要覆盖，每个 window 例外都配 boundary 探针。
- dev 和 test 各至少 60 对 contrast pair：两个 episode 只在某个事件里一条较早的用户消息不同，之后的消息完全相同，gold 转移不同；用 `contrast_group` 标出。train 里也要有一些。
- 同一个 episode 里要有“例外再修订”和“先加例外、再改一般偏好、例外仍然有效”这类多步链条，不能每个事件都是孤立的。

## 质量要求（重点）
1. **对话自然**：像真实用户和助手的对话，带无关闲聊和干扰信息。任何人都不能说出打标签的规则或替模型下结论（例如 "I won't guess"、"everything else stays as it was"、"this is an exception"、"treat this as the default"）。助手不能复述正确答案或替用户做决定。
2. **不留捷径**：exception、default、usual、always、only、for now、temporary、one-off、remember、save 这类词要在写入类和不写入类事件里都出现。`audit.py` 要跑一个“只看最后一条用户消息”的词袋分类探针并报告准确率；在 contrast pair 上，只看最后 k 条消息的方法最多对一半。
3. **标签唯一**：每个事件只有一种正确的状态变化，不能出现“删掉和改写都算对”的情况。撤销例外一律是 `exception_retirement`（回到继承一般偏好），不能把当前一般偏好复制成一条固定例外。同一个探针最多只有一个例外适用（protocol §8）。
4. **类别语义按 protocol §3**：`stable_preference` 包括一次性请求、别人的或引用的偏好、假设、被拒绝的建议、重申；`clarify` 只用于用户确实没定目标或期限，后续事件里通常会澄清。
5. **划分隔离**：train / dev / test 的属性、scope 短语、取值、场景家族和措辞模板全部不重叠。`validate.py` 检查这些集合两两不相交，并报告 test 与 train 对话之间最长的公共单词 n-gram。
6. **多样性**：至少 80 个不同属性（各划分不重复），覆盖出行、饮食、工作习惯、设备设置、通知、文档格式、购物、运动等领域；用户人设、语气和句子长短有变化；取值和 scope 都是自然的英文短语；日期写在对话里时用自然说法（"next Monday"、"through the 24th"），gold 用 ISO 日期。
7. **只用虚构内容**：不出现真实人名、品牌、地址或任何个人信息。
8. **不复用旧数据**：40 条 smoke、24 条候选评测、v0.1、v0.2 的对话、领域和措辞都不能出现。

## validate.py 必须检查
- 格式完全符合 protocol §1；角色交替、用户先说；事件日期严格递增；所有 id 唯一。
- 每个事件的 `state_after` 相对前一状态的变化恰好符合它的类别，`decision` 与类别一致，`evidence_message` 指向本事件里的一条用户消息。
- 每个探针：`after_event` 存在；`options` 含 `gold`；`gold` 等于按 protocol §8 从当时状态算出的值；最多一个例外适用。
- 对话里不出现 gold、category、scope_key 等字段名或其取值。
- 对每个 episode 调用 `scope_memory.protocol.replay_gold(episode)`（import 前把快照根目录加进 `sys.path`），必须全部通过。也可以在快照根目录直接运行 `python -m scope_memory.protocol check training\scope_revision_v1\data\train.jsonl training\scope_revision_v1\data\dev.jsonl training\scope_revision_v1\data\test.jsonl`。
- 所有产出文件都是 LF 换行；重新运行 `build.py` 的结果与 `data\` 逐字节一致。

## 完成后报告
各划分的规模和类别分布、每项检查的结果、捷径探针数字、最长公共 n-gram、已知局限，以及没做到的要求。不要说数据“已验证可用于训练”，只说哪些检查通过了。

## Feedback that produced v1.1

v1 passed the contract checks (replay_gold 920/920, generator validation, contrast pairs). Requested changes, all other requirements unchanged:
1. Randomize event structure: vary the order and number of categories, let some episodes skip categories, use two attributes in about 30% of episodes, 4–8 events at random. Target: a majority baseline on event position plus the number of exceptions in memory scores at most 35% on test (v1: 61%).
2. De-template assistant turns: at least 1,500 distinct assistant messages in train (v1: 177); avoid questions that ask the label dimension directly; sometimes the user volunteers the information unprompted.
3. Users name the attribute verbatim in at most 40% of events (v1: 100%); add the natural paraphrases to `value_aliases` and scope aliases so replay_gold still reads the state back.
4. Fewer lexical cues: a last-user-message bag-of-words classifier scores at most 40% on test (v1: 55.75%); no phrase that occurs in only one category covers more than 15% of that category's events.
5. Keep the protocol, split isolation, contrast pairs, LF line endings and byte-identical rebuild, and report the baselines of points 1 and 4 in `audit.json`.

Measured on v1.1 (test): position plus exceptions 28.7%, last user message 28.8% (majority 17.7%); 1,772 distinct assistant messages in train; attribute named verbatim in 17.6% of events; 30% two-attribute episodes.

## Protocol 1.2 (2026-11-16)

Gold writes now copy the user's words (protocol §6), so the user's messages must name every new value and every new situation in a listed form: the catalog name or one of its aliases. v1.1 meets this without changes: across all splits, each of the 2,947 values written is named in the evidence message, and each of the 1,001 new situations in a user message (913 in the evidence message). The user uses the catalog name itself in about half of the writes. `replay_gold` rejects any event that breaks this, so new data must keep it.
