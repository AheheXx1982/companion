---
title: 标的（Tickers）
created: 2026-06-16
updated: 2026-06-16
type: entity
tags: [primary-course, intermediate-course, tickers, liquidity, iv-rank, wheel, csp]
sources: [D:\obsidian-vault\知识库\1.初级期权课程\第7章_保证金制度和期权的流动性\0702_第十七讲：拥有一票否决权的期权流动性.md]
confidence: high
contested: false
contradictions: []
---

# 标的（Tickers）

选对标的，是期权策略成功的“第一道门槛”。流动性、波动率和基本面共同决定一个股票/ETF 是否适合作为期权交易标的。

## 核心筛选标准

- 期权流动性：买卖深度（Open Interest / Volume）是否充足；流动性不足会导致滑点大、无法按理论价成交、行权风险上升。
- 波动率特征：IV Rank / IV Percentile 是否稳定；低波动标的可能长期缺乏卖权机会，高波动标的则 Box 风险大。
- 基本面稳健性：收入、现金流和资产负债表能否支撑股价稳健运行；长期[[entities/strategies| Wheel]] 需要避免“接股即暴雷”的情况。
- 市值与机构关注度：大市值蓝筹/ETF 更适合期权新手，小市值股票的流动性陷阱和财报爆雷风险更高。

## 常见参与层级

- 高流动性大盘股/ETF：如标普 500 ETF（SPY）、纳斯达克 ETF（QQQ）——流动性最好，IV 稳定，但权利金绝对值偏低。
- 优质蓝筹股：股息可观的龙头公司，适合[[workflows/wheel| Wheel]]和[[workflows/pmcc| PMCC]]长期循环。
- 中等市值成长股：波动率更高、IV 更贵，适合更高阶策略，但对研究深度要求也更高。

## 选股流程（参考）

1. 筛选 IV Rank 处于中等偏高区间。
2. 确认期权链 Open Interest ≥ 1000。
3. 检查近 4 个季度是否出现异常波动或持续性利空。
4. 若同时满足，纳入候选；否则淘汰或降级观察。

## 与策略的关系

- [[workflows/wheel| Wheel]]依赖长期稳定的标的，因此标的基本面必须过关。
- [[workflows/csp-selection| CSP 筛选]]比 Wheel 更激进，允许更高波动率，但仍需流动性备兑。

> **出处**：内容整合自初级课程保证金、流动性与选股相关章节（^[课程:D:\obsidian-vault\知识库\1.初级期权课程\第 7 章_保证金制度和期权的流动性\0702_第十七讲：拥有一票否决权的期权流动性.md]）。
