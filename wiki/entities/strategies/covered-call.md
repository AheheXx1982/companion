---
title: Covered Call（备兑看涨期权）
created: 2026-06-16
updated: 2026-06-16
type: entity
tags: [primary-course, intermediate-course, advanced-course, strategies, covered-call, income, yield, wheel]
sources:
  [
    D:\obsidian-vault\知识库\1.初级期权课程\第6章_期权的作用和案例展示\0603_第十五讲：期权的基本作用三 -- 收权利金.md,
    D:\obsidian-vault\知识库\3.高级期权课程\第2章_个股价值投资策略\0201_第十四讲：颠覆你认知的Covered Call策略.md,
  ]
confidence: high
contested: false
contradictions: []
---

# Covered Call（备兑看涨期权）

Covered Call（简称 CC）是期权策略中流行度最高、最直接的“卖租模式”：持有正股，卖出虚值 Call，换取权利金。

## 定义与核心逻辑

- 正股 backed：持有正股提供“担保”，锁定卖 Call 义务。
- 收取权利金：将存量仓位变成持续收租资产，收益来源包括股息+租金。
- 收益封顶：正股价格超过 Call 行权价后，超出部分被行权抵扣。

## 适用条件

- 账户必须有对应数量正股（100 股/张）。
- 市场环境：震荡或温和上涨；单边暴涨时容易因正股上行过快导致 Call 被指派。
- 标的资格：流动性好、基本面稳健的股票/ETF。

## 与平价公式的关系

- 从[[concepts/pricing|期权平价公式]]视角，Covered Call = Protective Put 的等价组合。
- 理解平价角度后，可将 CC 放入统一的策略管理框架，而非孤立技巧。

## 实操要点

- 行权价选择：Delta 0.2-0.35 的 OTM Call，平衡收入与正股保留。
- 到期周期：30-60 天分阶段滚动，确保时间价值加速衰减时持续收租。
- 被行权处理：正股已赚过资本增值，被 Call 走是“兑现”，不是“错过”。

## 高级应用（高级课程）

- CC 的局限：大涨踏空、暴跌套牢、长期震荡被磨损。
- CC 的变通：用 PMCC 替代正股，或用 Spread 限制上行暴露。
- CC 与 Wheel 的衔接：被 Call 走后重新卖 Put，开启新 Wheel 循环。

## 风险管理

- 禁止裸卖：没有正股就卖 Call 等于无限风险。
- 单一标的集中度风险：若正股暴雷，租金无法抵消亏损。
- 事件前审查：财报、宏观事件前可暂停卖新 Call，降低指派风险。

> **出处**：内容整合自初级课程收权利金与高级课程 CC 策略章节（^[课程:D:\obsidian-vault\知识库\1.初级期权课程\第 6 章_期权的作用和案例展示\0603_第十五讲：期权的基本作用三 -- 收权利金.md]、^[课程:D:\obsidian-vault\知识库\3.高级期权课程\第 2 章_个股价值投资策略\0201_第十四讲：颠覆你认知的 Covered Call 策略.md]）。
