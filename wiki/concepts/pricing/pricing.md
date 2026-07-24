---
title: 期权定价
created: 2026-06-16
updated: 2026-06-16
type: concept
tags: [primary-course, intermediate-course, advanced-course, pricing, bsm, synthetic, cash-secured, margin]
sources:
  [
    D:\obsidian-vault\知识库\1.初级期权课程\第8章_Covered Call和Put Call Parity\0802_第十九讲：期权平价公式让Put和Call灵活转换.md,
    D:\obsidian-vault\知识库\1.初级期权课程\第9章_影响期权价格的因素 -- BSM模型和IV\0901_第二十讲：期权的定价公式 -- BSM模型.md,
  ]
confidence: high
contested: false
contradictions: []
---

# 期权定价

期权定价建立在数学关系与市场供需之上。理解定价，才能判断期权“贵了还是便宜了”，进而决定何时卖权、何时买权。

## 核心定价框架

- 内在价值：立即行权所能得到的价值；ITM 期权才具备。
- 时间价值：超越内在价值的部分；随到期临近衰减，在 ATM 附近最高。
- 波动率价值：由[[concepts/volatility|隐含波动率]]决定，代表市场对未来不确定性的定价。

## 关键定价公式

- BSM（Black-Scholes-Merton）模型：用标的价、行权价、剩余时间、无风险利率和 IV 计算理论价格。
- Put-Call Parity（期权平价公式）：`Call + 行权价折现值 = Put + 正股`；是判断期权定价偏离的基准线。

##定价偏离的实战意义

- 当市场价格显著偏离平价公式时，存在套利空间；散户不必复杂执行，但可用来判断期权相对贵贱。
- 合成仓位（Synthetic）基于平价公式：用期权复制正股或另一期权，在流动性差异中找到更优执行路径。

## 与策略的关系

- [[entities/strategies|Covered Call]] 和 Protective Put 在平价视角下存在等价关系，理解后可将策略体系统一。
- [[workflows/csp-selection|CSP]] 的选择需要判断 Put 是否“划算”：IV 高位时卖 Put 更有吸引力，意即在定价视角上更便宜卖给买方。

> **出处**：内容整合自初级课程平价公式与 BSM/IV 体系（^[课程:D:\obsidian-vault\知识库\1.初级期权课程\第 8 章_Covered Call 和 Put Call Parity\0802_第十九讲：期权平价公式让 Put 和 Call 灵活转换.md]、^[课程:D:\obsidian-vault\知识库\1.初级期权课程\第 9 章_影响期权价格的因素 -- BSM 模型和 IV\0901_第二十讲：期权的定价公式 -- BSM 模型.md]）。
