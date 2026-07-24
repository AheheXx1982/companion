---
title: 希腊字母（Greeks）
created: 2026-06-16
updated: 2026-06-16
type: concept
tags: [primary-course, intermediate-course, greeks, delta, gamma, theta, vega, risk, pricing]
sources:
  [
    D:\obsidian-vault\知识库\1.初级期权课程\第9章_影响期权价格的因素 -- BSM模型和IV\0903_第二十二讲：如何运用隐含波动率IV的性质.md,
  ]
confidence: high
contested: false
contradictions: []
---

# 希腊字母（Greeks）

希腊字母用于量化解释期权价格对各种因子的敏感度。它们是[[concepts/pricing|期权定价]]与[[concepts/volatility|波动率]]分析的基础工具，也是风险管理的核心语言。

## 核心希腊字母

- Delta（δ）：标的资产价格变动 1 美元时，期权价格的预期变化幅度；也近似为到期时处于虚值状态的概率。
- Gamma（γ）：Delta 对标的资产价格的二次敏感度；Delta 变化越快，Gamma 越大， ATM 附近 Gamma 最高。
- Theta（θ）：时间衰减速度；代表在其他条件不变时，期权价格每天因时间流逝而损失的价值。
- Vega（Vega）：隐含波动率变动 1 个点时，期权价格的预期变化幅度；事件前和恐慌时，Vega 的影响最显著。

## 辅助指标

- Rho（ρ）：利率变动对期权价格的影响；在长期 LEAP 中更值得关注，日常交易中相对次要。
- Vanna：Vega 对标的资产价格变动的敏感度；属于高阶 Greeks，实际对冲时才会用到。

## 与策略的关联

- [[entities/strategies|卖方策略]]更关注 Theta 和 Vega：希望时间加快流逝，并利用 IV 高位时入场。
- [[entities/strategies|买方策略]]更关注 Delta 和 Gamma：希望在 IV 低位时买入，等待标的大幅移动。
- 在[[workflows/wheel| Wheel 策略]]中，管理 Theta 是核心，Vega 用于判断何时该继续卖权、何时该等待。

##避险启示

风险管理的第一步不是计算盈亏，而是理解 Greeks 的交互影响：高 Theta 的短期权若叠加高 Gamma，盘中回撤会被快速放大。

> **出处**：概念体系整合自初级课程 BSM/IV 相关讲义（^[课程:D:\obsidian-vault\知识库\1.初级期权课程\第 9 章_影响期权价格的因素 -- BSM 模型和 IV\0903_第二十二讲：如何运用隐含波动率 IV 的性质.md]）。
