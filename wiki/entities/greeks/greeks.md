---
title: 希腊字母（Greeks）
created: 2026-06-16
updated: 2026-06-16
type: entity
tags: [primary-course, intermediate-course, advanced-course, greeks, delta, gamma, theta, vega, risk, pricing]
sources:
  [D:\obsidian-vault\知识库\1.初级期权课程\第9章_影响期权价格的因素 -- BSM模型和IV\0901_第二十讲：期权的定价公式 -- BSM模型.md]
confidence: high
contested: false
contradictions: []
---

# 希腊字母（Greeks）

本页汇总初/中级课程中 Greeks 的核心定义、页面入口及其在策略执行中的角色。

## 核心希腊字母

- Delta（δ）：正股价格变动时期权价格的预期变化；方向敏感度。
- Gamma（γ）：Delta 的方向变化率；ATM 区间最大，方向突变时影响显著。
- Theta（θ）：时间衰减；期权价格在到期日前每天的自然损耗。
- Vega（Vega）：IV 变化对期权价格的影响；事件前和恐慌时 Vega 高。

## 辅助指标

- Rho（ρ）：利率敏感度；对长期合约影响更大。
- Vanna：Vega 对正股的二次波动；高阶对冲使用。

## 与策略的关联

- [[entities/strategies/covered-call| Covered Call]]、[[entities/strategies/cash-secured-put| CSP]] 更关注 Theta 和 Vega：希望时间快速衰减，并利用 IV 高位获得高权利金。
- 买方策略（如 [[entities/strategies/pmcc| PMCC]] 中的 LEAP）更关注 Delta 和 Gamma：方向性暴露与加速行情利用。
- [[entities/volatility| 波动率]] 页面解释了 IV 与 Vega 的联合作用。
- [[concepts/pricing| 定价]] 页面里，Greeks 是对 BSM 输入变量的解释形式。

> **出处**：内容整合自初级课程 BSM 与 Greeks 章节（^[课程:D:\obsidian-vault\知识库\1.初级期权课程\第 9 章_影响期权价格的因素 -- BSM 模型和 IV\0901_第二十讲：期权的定价公式 -- BSM 模型.md]）。
