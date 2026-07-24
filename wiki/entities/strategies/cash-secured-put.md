---
title: Cash Secured Put（现金备兑看跌期权）
created: 2026-06-16
updated: 2026-06-16
type: entity
tags: [primary-course, intermediate-course, advanced-course, strategies, cash-secured-put, wheel, csp, income, yield]
sources: [D:\obsidian-vault\知识库\1.初级期权课程\第6章_期权的作用和案例展示\0603_第十五讲：期权的基本作用三 -- 收权利金.md]
confidence: high
contested: false
contradictions: []
---

# Cash Secured Put（现金备兑看跌期权）

Cash Secured Put（简称 CSP）是最基础的正股“低成本接入口”：卖 Put，收取权利金，行权则按约定价买入正股。

## 定义与核心逻辑

- 现金备兑：在账户中预留等额行权资金，作为“就能位”担保。
- 收取权利金：卖 Put 收到保费，若未行权则纯收入。
- 接股计划价：被行权后的正股买入价 = 行权价 − 已收权利金，成本已打折。

## 适用条件

- 账户内有充足现金，不被挪用。
- 愿意并以计划价持有该正股：若暴跌或基本面恶化，需放弃接股并接受亏损。

## 实操要点

- 行权价选择：Delta 0.2-0.35；即正股现价下方 5%-15%。
- 到期周期：30-45 天，不宜拖太长。
- 历史胜率：若正股基本面稳健、IV 中等偏高，长期胜率可达 70%-80%。

## 与&#8203;[[entities/strategies/wheel| Wheel 策略]]的衔接

- CSP 是 Wheel 的“接股端”：Wheel 的起点几乎都是卖 Put。
- Wheel 标准化要求：CC 与 CSP 在同一标的上须 1:1 股/张匹配，避免裸卖敞口。

## 与平价公式的视角

- 从 Put-Call Parity 角度看：买正股 + 买 Put = 裸买 Call；卖 Put 可看作折价版本。
- 理解平价视角后，可将 CSP 纳入更完整的“买股/买权/组合决策”体系。

## 风险管理

- 现金专款专用：不能挪用，否则接股风险升高。
- 放弃原则：若正股基本面持续恶化，即使到了行权日也可以选择放弃行权，接受已收权利金覆盖部分亏损。
- 集中度控制：单笔 CSP 建议不超过账户净值的 1%-2%。

> **出处**：内容整合自初级课程收权利金与策略章节（^[课程:D:\obsidian-vault\知识库\1.初级期权课程\第 6 章_期权的作用和案例展示\0603_第十五讲：期权的基本作用三 -- 收权利金.md]）。
