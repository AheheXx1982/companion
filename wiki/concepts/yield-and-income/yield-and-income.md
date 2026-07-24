---
title: 收益与收入（Yield and Income）
created: 2026-06-16
updated: 2026-06-16
type: concept
tags: [primary-course, intermediate-course, advanced-course, yield, income, covered-call, cash-secured-put, wheel, dividend]
sources: [D:\obsidian-vault\知识库\1.初级期权课程\第6章_期权的作用和案例展示\0603_第十五讲：期权的基本作用三 -- 收权利金.md]
confidence: high
contested: false
contradictions: []
---

# 收益与收入（Yield and Income）

期权收益不仅是股价上涨的资本利得，更可持续的是通过时间价值衰减和权利金收入创造的现金流。

## 核心机制

- 权利金收入：卖出期权获得的即时现金流；本质是卖方向市场收取的风险溢价。
- 股息叠加：持有正股同时卖 Call 时，股息+权利金形成双现金流，提升综合收益率。
- 复合收益：[[workflows/wheel| Wheel 策略]]通过循环接股与卖权，实现长期复利。

## 关键策略角色

- [[entities/strategies|Covered Call]]：即收股息又收权利金，目标是提高持仓的整体 yield。
- [[entities/strategies|Cash Secured Put]]：卖 Put 收权利金，若被行权则按计划价接股，成本已扣除权利金。
- [[entities/strategies|PMCC]]：用低价 LEAP 替代正股后做 Covered Call，降低建仓资本，同时保留收权利金能力。

## 收益构成拆解

- 资本增值：正股本身的价格上涨。
- 股息：正股的分红现金流。
- 权利金：期权卖方的周期性收入。
- 行权利得/接股成本优化：被行权时的买入价已扣除权利金折扣。

## 收益目标设定

- 年化 15%-30% 权利金覆盖率是常见初级目标。
- 实际 yield 要根据账户规模、标的波动率和 IV 水平动态调整。
- 复合增长需要长期纪律：每月滚动、每季度再平衡，不因短期 IV 下行而中断节奏。

## 风险与理念

- 追求高 yield 不等于规避风险；高 sell strike 可能带来接股风险或正股被 Call 走的收益封顶。
- 最安全的 yield 来自有正股 backed 的卖方组合，拒绝裸卖。

> **出处**：内容整合自初级课程收权利金章节（^[课程:D:\obsidian-vault\知识库\1.初级期权课程\第 6 章_期权的作用和案例展示\0603_第十五讲：期权的基本作用三 -- 收权利金.md]）。
