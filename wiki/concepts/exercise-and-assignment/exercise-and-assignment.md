---
title: 行权与指派（Exercise and Assignment）
created: 2026-06-16
updated: 2026-06-16
type: concept
tags: [primary-course, intermediate-course, exercise, assignment, margin, cash-secured, covered-call]
sources:
  [
    D:\obsidian-vault\知识库\1.初级期权课程\第7章_保证金制度和期权的流动性\0701_第十六讲：怎么看账户保证金保证金对于期权交易的意义.md,
  ]
confidence: high
contested: false
contradictions: []
---

# 行权与指派（Exercise and Assignment）

期权到期时，买方可以主动行权，卖方则可能被自动指派。理解两者的权利与义务，是避免意外仓位和保证金的根本前提。

## 核心定义

- Exercise（行权）：期权买方主动要求按约定价格买入或卖出标的资产；买方拥有选择权。
- Assignment（指派）：期权卖方被券商系统授权履行义务；被指派是卖出权的必然风险。

## 常见指派场景

- [[entities/strategies|Cash Secured Put]] 被指派：按行权价买入正股；前提是有预留现金。
- [[entities/strategies|Covered Call]] 被指派：按行权价卖出正股；前提是已持有对应数量的正股。

## 与保证金的关系

- 在保证金账户中，某些情况下未被充分[[concepts/pricing|备兑]]的卖方仓位可能被自动结算，带来保证金追缴。
- 现金备兑（Cash Secured）和正股备兑（Covered）是避免指派意外的最低标准。

## 可行权条件的实务判断

- 到期的 ITM 期权通常会被行权/指派；期权交易所会自动处理，但深度 ITM 时会出现流动性不足导致的执行风险。
- OTM 期权通常放弃行权，因为市场价更优；例行检查账户状态可提前发现异常。

## 风险与操作建议

- 卖方在到期日前确认备兑完整性（现金或正股是否到位）。
- 买方在到期前判断是否要行权，避免因忘记行权导致期权价值归零。

> **出处**：概念整合自初级课程保证金与流动性相关章节（^[课程:D:\obsidian-vault\知识库\1.初级期权课程\第 7 章_保证金制度和期权的流动性\0701_第十六讲：怎么看账户保证金保证金对于期权交易的意义.md]）。
