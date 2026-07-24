---
title: 波动率（Volatility）
created: 2026-06-16
updated: 2026-06-16
type: entity
tags: [primary-course, intermediate-course, advanced-course, volatility, iv, vega, hv, event-premium, mean-reversion]
sources:
  [
    D:\obsidian-vault\知识库\1.初级期权课程\第9章_影响期权价格的因素 -- BSM模型和IV\0902_第二十一讲：隐含波动率 Implied Volatility.md,
  ]
confidence: high
contested: false
contradictions: []
---

# 波动率（Volatility）

本页汇总初/中级课程中波动率的核心定义、页面入口与策略角色。

## 核心定义

- IV（Implied Volatility）：从期权价格反推出来的波动率预期；高 IV = 期权贵，低 IV = 期权便宜。
- HV（Historical Volatility）：过去实际波动率；与 IV 比较后，可判断期权被高估还是低估。
- VIX：标普 500 期权链的 ATM 30 日 IV；市场整体恐慌度的衡量。

## IV 特性

- 均值回归：IV 不会长期停留在极端位置，早晚回归均值。
- 急涨缓跌：恐慌时 IV 快速上升，但情绪修复时恢复缓慢。
- 事件溢价：财报/宏观事件前 IV 抬升，期权更贵。

## 与定价的关系

- 波动率是[[entities/pricing| 定价]]里时间价值的重要组成，决定期权“贵不贵”。
- Vega 是波动率敏感度量化；详见[[entities/greeks| 希腊字母]]页面。

## 与策略的关联

- 高 IV → 适合卖权（[[entities/strategies/covered-call| CC]] / [[entities/strategies/cash-secured-put| CSP]] / [[workflows/wheel| Wheel]]）。
- 低 IV → 适合买方（[[entities/strategies/pmcc| PMCC]] LEAP、价差买方）。
- 事件前 IV 抬升：不新建仓位，优先事件后 IV Crush 时重启卖权。

> **出处**：内容整合自初级课程 IV 相关章节（^[课程:D:\obsidian-vault\知识库\1.初级期权课程\第 9 章_影响期权价格的因素 -- BSM 模型和 IV\0902_第二十一讲：隐含波动率 Implied Volatility.md]）。
