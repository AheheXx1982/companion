---
title: PMCC（穷人 Covered Call，Poor Man's Covered Call）
created: 2026-06-16
updated: 2026-06-16
type: workflow
tags: [primary-course, intermediate-course, workflow, pmcc, covered-call, leap, iv, delta]
sources:
  [
    D:\obsidian-vault\知识库\1.初级期权课程\第8章_Covered Call和Put Call Parity\0802_第十九讲：期权平价公式让Put和Call灵活转换.md,
  ]
confidence: high
contested: false
contradictions: []
---

# PMCC（穷人 Covered Call，Poor Man's Covered Call）

PMCC 是用深度 ITM LEAP Call 替代正股，再叠加卖 Call 的组合策略。其核心是降低建仓资本占用，同时保留收租金的 Covered Call 特性。

## 必要性框架

- 正股买不起或资本效率要求高：一手正股可能耗尽大部分资金。
- LEAP Call 提供类似正股方向的 Delta：深度 ITM LEAP 的 Delta 接近 1，几乎等同于持仓正股。
- LEAP 时间价值高：买入 LEAP 时支付的时间价值，通过后续卖 Call 的租金持续回收。

## 核心结构

- 买入深度 ITM 的长期 LEAP Call（1-2 年到期，Delta 0.7-0.85，行权价低于正股现价）。
- 每个周期卖 1 张 OTM Call（30-60 天到期），收取权利金。
- LEAP 价值里的一部分时间价值，被卖 Call 的权利金持续回收。

## 参数选择

- LEAP 行权价：越深 ITM，Delta 越高，但 LEAP 价格越高；通常用现价下方 10%-20% 的行权价。
- 卖 Call 行权价：高于正股现价，Delta 0.2-0.35，争取被 Call 走的低概率。
- Delta 同步：卖 Call 的 Delta + LEAP 的 Delta ≈ 0.85-1.0 左右，整体仍偏正股方向。

## 优势与局限

优势：

- 资本效率高：LEAP 押金远低于等额正股。
- 时间价值回收：LEAP 的时间价值通过卖 Call 持续回流。
- 下行保护：正股下跌时，LEAP 亏损小于直接持有正股。

局限：

- LEAP 本身不是正股：若正股长期横盘或暴跌，LEAP 时间价值持续损耗。
- 行权费率和流动性：LEAP 相对正股流动性稍差，Deep ITM 买价可能偏高。
- 卖 Call 被指派风险：若正股暴涨上行，LEAP 的 Call 可能被提前指派，提前结束策略或需要换月。

## 执行规约

- 单手 LEAP 仅卖一张 Call；多手 LEAP 可按比例处理。
- LEAP 买入后不建议随意平仓：过早换月或平仓会造成 LEAP 时间价值不可逆损失。
- 选择 IV 相对合理时的深度 ITM 点：IV 过高的 LEAP 会造成时间价值过高，回收周期变长。

> **出处**：内容整合自初级课程平价公式与 LEAP/PMCC 章节（^[课程:D:\obsidian-vault\知识库\1.初级期权课程\第 8 章_Covered Call 和 Put Call Parity\0802_第十九讲：期权平价公式让 Put 和 Call 灵活转换.md]）。
