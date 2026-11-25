# 60 条类别审核：对比与最终仲裁记录

记录日期：2026-11-24

## 最终决定

Raina 在本次对话中确认：队友 C 已完成两处分歧的仲裁，均支持队友 A；采用 A 的全部 60 条类别标签作为最终人工标签。

最终文件：`labels_final.json`。其中 `annotator` 为 `final_adjudicated`，表示仲裁后的汇总结果，不表示 C 重新标注了全部 60 条。

| 编号 | Raina 原始标签 | A 原始标签 | C 的仲裁结果（由 Raina 转述） | 最终类别 |
|---|---|---|---|---|
| L008 | exception_revision | stable_preference | 支持 A | stable_preference |
| L024 | general_update | exception_revision | 支持 A | exception_revision |

其他 58 条两人原本一致，直接保留。两位标注者的原始文件不修改。

## 仲裁前的一致性

- 共同标注：60 条。
- 一致：58 条；分歧：2 条。
- 原始一致率：96.6667%。
- 原始 Cohen's kappa：0.9600。

这些指标由两份原始人工标签计算，不能用最终汇总标签重新计算后宣称两人原始一致率为 100%。本次统计未使用数据生成标签作为判断依据。

## 来源与记录边界

- Raina 原始文件：`Raina_finished/labels_raina.json`。
- A 原始文件：`annotator_A/labels_A.json`。
- C 的仲裁来源：Raina 在对话中的明确确认；本次未提供 C 的原始标注文件，未将本记录伪装为 C 的原始提交。
- 本记录不单独确认仲裁过程是否全程盲审。Raina 部分条目曾与 AI 讨论，应在研究方法或辅助记录中如实说明。
- 此次确定的是这 60 条的最终人工类别；未因此改写生成数据、重新训练模型或改变模型评测结果。

## 原始文件 SHA-256

- Raina：`3d162e9f56bc0c1ec4aa5250de967c9c93302731b13c558803e13f8901d82795`。
- A：`3ad4f1599af8b852833ee4b744eb148c2bbc5031eb521c674a3ac1b145d1dd7c`。
