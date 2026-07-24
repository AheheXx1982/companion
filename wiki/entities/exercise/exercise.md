---
title: 行权与指派（Exercise and Assignment）
created: 2026-06-16
updated: 2026-06-16
type: entity
tags: [primary-course, intermediate-course, exercise, assignment, cash-secured-put, covered-call, margin, workflow]
sources:
  [
    D:\obsidian-vault\知识库\1.初级期权课程\第7章_保证金制度和期权的流动性\0701_第十六讲：怎么看账户保证金保证金对于期权交易的意义.md,
  ]
confidence: high
contested: false
contradictions: []
---

# 行权与指派（Exercise and Assignment）

本页汇总初/中级课程中关于行权（Exercise）与指派（Assignment）的核心概念、页面入口与操作事宜。

## 核心概念

- Exercise（行权）：期权买方行使权利，按约定价格买入或卖出标的资产。
- Assignment（指派）：卖方被系统指定履行义务；卖 Put 被指派导致买入正股，卖 Call 被指派导致卖出正股。

## 典型场景

- [[entities/strategies/cash-secured-put| CSP]] 被指派：按行权价买入正股，现金被锁定为持股。
- [[entities/strategies/covered-call| Covered Call]] 被指派：按行权价卖出正股，获得权利金+正股卖出收入。

## 与保证金的关系

- 若备兑不足（无正股或现金），可能出现保证金追缴；这是风险控制的第一道防线。
- 现金备兑和正股备兑的最低条件是策略长期存活的基本保障。

## 实务检查点

- 到期前：确认备兑完整性。
- 深度 ITM：流动性不足会导致指派结果比预期更大。
- OTM 期权通常不选择行权；但需警惕 ITM 而未被主动行权时账户状态异常。

> **出处**：内容整合自初级课程保证金章节（^[课程:D:\obsidian-vault\知识库\1.初级期权课程\第 7 章_保证金制度和期权的流动性\0701_第十六讲：怎么看账户保证金保证金对于期权交易的意义.md]）。
