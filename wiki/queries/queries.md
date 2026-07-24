---
title: 查询示例（Queries）
created: 2026-06-16
updated: 2026-06-16
type: query
tags: [meta, query, workflow, scheduler, llm, options]
sources: []
confidence: high
contested: false
contradictions: []
---

# 查询示例（Queries）

本页用于记录本 wiki 可支持的可查询模式、典型 LLM 问题及对应的 wiki 页面入口路径。

## 推荐链接路径

- 策略入门：`entities/strategies/strategies` → 细读对应策略页面
- 标的筛选：`entities/tickers` → 结合 `workflows/csp-selection` 的漏斗流程
- 定价判断：`entities/pricing` 与 `entities/greeks` → 再回到 `entities/volatility` 判断贵贱
- 执行流程：`workflows/wheel` / `workflows/pmcc` / `workflows/csp-selection`

## 典型问题

1. “我只有少量资金，如何开始卖权收租？” → 先读 `entities/strategies/pmcc`，再读 `workflows/csp-selection`。
2. “如何判断现在适不适合卖权？” → 读 `entities/volatility` + `entities/greeks` + `workflows/csp-selection`。
3. “Wheel 的具体执行节奏是什么？” → 直接看 `workflows/wheel`，并回看 `entities/strategies/cash-secured-put` 与 `entities/strategies/covered-call`。
4. “策略 A 与策略 B 有哪些区别？” → 先到 `comparisons/strategy-vs-strategy`， Entscheidungsregeln 已建立。
5. “行权或指派时的账户风险有哪些？” → 先读 `entities/exercise`，再回到对应策略页面复核备兑状态。
