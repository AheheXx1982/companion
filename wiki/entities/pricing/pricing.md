---
title: 定价（Pricing）
created: 2026-06-16
updated: 2026-06-16
type: entity
tags: [primary-course, intermediate-course, advanced-course, pricing, bsm, put-call-parity, synthetic, valuation]
sources:
  [
    D:\obsidian-vault\知识库\1.初级期权课程\第8章_Covered Call和Put Call Parity\0802_第十九讲：期权平价公式让Put和Call灵活转换.md,
  ]
confidence: high
contested: false
contradictions: []
---

# 定价（Pricing）

定价是期权估值与交易决策的底层逻辑。本页汇总初/中级课程中定价相关核心概念与页面入口。

## 核心概念

- 内在价值：立即行权价值的即时变现部分；ITM 期权才有。
- 时间价值：期权价格中超越内在价值的部分，随到期临近衰减，在 ATM 附近最高。
- 波动率价值：由[[entities/volatility|隐含波动率]]主导，代表市场对未来的不确定定价。

## 核心公式

- BSM（Black-Scholes-Merton）模型：用于推导理论价格与 Greeks；输入包括正股价、行权价、时间、利率、IV。
- Put-Call Parity：`C + K·e⁻ʳᵗ = P + S`；平价偏离是判断期权贵贱的基准。

## 与策略的关联

- [[workflows/csp-selection| CSP 筛选]]依赖对 Put 定价的判断：IV 高位时卖 Put 更有利。
- [[entities/strategies/wheel| Wheel 策略]]在定价视角下是“双备兑 + 双现金流”包的循环执行。
- [[entities/strategies/pmcc| PMCC]]将 LEAP 作为长期正股替代，定价精度对建仓成本影响很大。

## 实务用途

- 判断“贵不贵”：用 IV Percentile / IV Rank 相对衡量，而不是孤立的绝对值。
- 套利偏离识别：不必真正做转换/逆转，但理解偏离可提高交易纪律。

> **出处**：内容整合自初级课程平价公式定价相关章节（^[课程:D:\obsidian-vault\知识库\1.初级期权课程\第 8 章_Covered Call 和 Put Call Parity\0802_第十九讲：期权平价公式让 Put 和 Call 灵活转换.md]）。
