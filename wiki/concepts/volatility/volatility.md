---
title: 波动率（Volatility）
created: 2026-06-16
updated: 2026-06-16
type: concept
tags: [primary-course, intermediate-course, advanced-course, volatility, iv, vega, hv, mean-reversion, event-premium]
sources:
  [
    D:\obsidian-vault\知识库\1.初级期权课程\第9章_影响期权价格的因素 -- BSM模型和IV\0903_第二十二讲：如何运用隐含波动率IV的性质.md,
  ]
confidence: high
contested: false
contradictions: []
---

# 波动率（Volatility）

波动率是期权定价中最关键的变量，也是“通过波动率赚钱”的核心工具。理解波动率，才能判断期权何时贵、何时便宜，以及如何在不同市场环境下调整策略。

## 核心定义

- 隐含波动率（IV, Implied Volatility）：从期权市场价格反推出来的波动率预期；是期权当前的“情绪温度计”，也是期权的“市盈率”。
- 历史波动率（HV, Historical Volatility）：基于历史股价计算得出的实际波动率；与 IV 对比，可判断期权被高估还是低估。
- VIX（恐慌指数）：标普 500 期权链的 ATM 30 日 IV 加权值；市场恐慌度的晴雨表。

## IV 三大特性

- 均值回归：IV 不会永远停留在极端位置，早晚会回到自身平均水平；越不回归，回归空间越大。
- 急涨缓跌：IV 对利空和恐慌反应剧烈、上升快；但对利好和恢复反应平缓、下降慢。
- 事件溢价：财报、宏观数据等事件前，IV 会因不确定性提前抬升，导致期权更贵。

## 波动率与策略的互动

- [[entities/strategies|卖方策略]]（Covered Call、Cash Secured Put）在 IV 高位时更优：用贵期权换取高权利金。
- [[entities/strategies|买方策略]]（Leap 买 Call、买 Put）在 IV 低位时更优：低成本建立方向性敞口。
- [[workflows/wheel| Wheel 策略]]的节奏受 IV 驱动：IV 高位时加快卖权频率，IV 低位时暂停或减仓。

## 波动率与 Greeks 的联动

- [[concepts/greeks|Vega]] 衡量 IV 变动对期权价格的影响；IV 越高，Vega 越大。
- 高 IV + 高 Vega = 期权对波动率极度敏感；适合做波动率交易者的观察指标。
- 高 IV + 高 Theta = 卖方“甜蜜点”：时间衰减快，且还能收高权利金。

## 避险启示

不要把 VIX 见顶当成股价见底；恐慌时最贵的是期权，不是股票。想买权，等事件落地后 IV 回落；想卖权，在 IV 到达极端高位但事件即将落地时动手。

> **出处**：概念体系整合自初级课程 IV 三特性章节（^[课程:D:\obsidian-vault\知识库\1.初级期权课程\第 9 章_影响期权价格的因素 -- BSM 模型和 IV\0903_第二十二讲：如何运用隐含波动率 IV 的性质.md]）。
