---
title: 策略对比（Strategy vs Strategy）
created: 2026-06-16
updated: 2026-06-16
type: comparison
tags: [primary-course, intermediate-course, advanced-course, comparison, covered-call, cash-secured-put, wheel, pmcc]
sources:
  [
    D:\obsidian-vault\知识库\3.高级期权课程\第2章_个股价值投资策略\0205_第十八讲：CC策略 vs Sell Put策略.md,
    D:\obsidian-vault\知识库\3.高级期权课程\第2章_个股价值投资策略\0204_第十七讲：CC策略的局限性.md,
  ]
confidence: high
contested: false
contradictions: []
---

# 策略对比（Strategy vs Strategy）

策略选择不是竞猜，而是根据自身目标、账户规模和市场环境做取舍。本页汇总常用策略的对比维度。

## 常见对比对

| 维度         | Covered Call (CC)            | Cash Secured Put (CSP) | Wheel 策略              | PMCC                         |
| ------------ | ---------------------------- | ---------------------- | ----------------------- | ---------------------------- |
| 资本占用     | 中（需持正股）               | 中（需预留现金）       | 中（需持正股+预留现金） | 低（用 LEAP 替代正股）       |
| 收益来源     | 股息+权利金                  | 权利金                 | 股息+权利金+复利        | 股息（或替代股息）+权利金    |
| 最大风险     | 正股下跌+Call 被指派导致兑现 | 正股暴跌接股           | 双循环压力+单标的集中   | LEAP 时间价值衰减+方向性亏损 |
| 最佳市场环境 | 震荡/温和上涨                | 震荡/温和上涨          | 长期震荡                | 长期上涨；适合长期牛市       |
| 时间管理     | 30-60 天滚动                 | 30-45 天滚动           | 按 CC+CSP 自动周期      | 1-2 年 LEAP + 月度 Call      |

## 高级策略对比

- SBS vs Covered Call：SBS 用 Put 组合替代正股，资本占用更低，但需要更高的执行精度；CC 更直觉、更容易维持纪律。
- Wheel vs 单策略：Wheel 是 CC 与 CSP 的循环叠加，收益更稳定，但占用资金时间更长，不适合需要快速回本的场景。

## 选择逻辑

- 希望“不接股、持续收租”：CC 最简单直接。
- 希望“接好股、降低成本”：CSP 为主。
- 希望“长期循环、复利增长”：Wheel。
- 希望“降低起步资金、仍想收租”：PMCC。

> **出处**：策略对比内容整合自高级课程 CC vs Sell Put 与 CC 局限性相关章节（^[课程:D:\obsidian-vault\知识库\3.高级期权课程\第 2 章_个股价值投资策略\0205_第十八讲：CC 策略 vs Sell Put 策略.md]、^[课程:D:\obsidian-vault\知识库\3.高级期权课程\第 2 章_个股价值投资策略\0204_第十七讲：CC 策略的局限性.md]）。
