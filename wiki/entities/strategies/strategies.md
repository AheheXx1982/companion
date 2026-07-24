---
title: 策略（Strategies）
created: 2026-06-16
updated: 2026-06-16
type: entity
tags:
  [
    primary-course,
    intermediate-course,
    advanced-course,
    strategies,
    covered-call,
    cash-secured-put,
    wheel,
    pmcc,
    protective-put,
    synthetic,
  ]
sources:
  [
    D:\obsidian-vault\知识库\1.初级期权课程\第6章_期权的作用和案例展示\0603_第十五讲：期权的基本作用三 -- 收权利金.md,
    D:\obsidian-vault\知识库\1.初级期权课程\第8章_Covered Call和Put Call Parity\0802_第十九讲：期权平价公式让Put和Call灵活转换.md,
  ]
confidence: high
contested: false
contradictions: []
---

# 策略（Strategies）

策略是期权知识体系中最直接可复用、可复盘的单元。理解每个策略的底层逻辑，而不是记忆符号，才能在不同市场环境中灵活调用。

## 基础定义

- 正股 Backed 原则：所有卖方策略都必须对应正股或现金预留，拒绝裸卖。
- 方向性策略：押注正股上涨、下跌或横盘。
- 波动率策略：押注 IV 扩张或收缩，而非标的方向。
- 收入策略：以持续收取权利金为主要目标。

## 常见策略汇总

- [[entities/strategies/covered-call| Covered Call (CC)]]：持有正股 + 卖 OTM Call，换取权利金并接受收益封顶。
- [[entities/strategies/cash-secured-put| Cash Secured Put (CSP)]]：预留现金 + 卖 Put，获得接股机会和权利金。
- [[entities/strategies/wheel| Wheel 策略]]：CSP 接股后转 CC，再继续卖 CSP，形成循环生产现金流。
- [[entities/strategies/pmcc| PMCC (Poor Man's Covered Call)]]：用深度 ITM LEAP 替代正股做 CC，降低建仓资本占用。
- [[entities/strategies/synthetic| 合成仓位（Synthetic）]]：基于平价公式用期权复制正股或另一期权，实现低成本对冲或替代。

## 高级扩展策略（高级课程）

- SBS（Sell Buy Spread）：卖 Put + 买 Put 的组合，最大化卖方优势、尾部风险可控。
- Collar：持正股 + 买 Put 保护 + 卖 Call 补贴，形成低成本对冲组合。
- Straddle / Strangle：同到期日同/不同行权价的 Call+Put 组合，用于方向性或波动率押注。
- Spread（价差）：两条不同行权价或到期日的期权组合，限制风险敞口。

## 策略选择框架

- 高 IV：优先卖权策略（CC、CSP、SBS、PMCC）。
- 低 IV：优先买方策略（长 Vega 的价差或 LEAP）。
- 震荡市：Wheel 和 Covered Call 最稳定。
- 财报/事件前：单腿买方或保护性对冲；事件后 IV Crush 适合重启卖权。

> **出处**：内容整合自初级课程期权平价、收权利金及策略体系章节（^[课程:D:\obsidian-vault\知识库\1.初级期权课程\第 6 章_期权的作用和案例展示\0603_第十五讲：期权的基本作用三 -- 收权利金.md]、^[课程:D:\obsidian-vault\知识库\1.初级期权课程\第 8 章_Covered Call 和 Put Call Parity\0802_第十九讲：期权平价公式让 Put 和 Call 灵活转换.md]）。
