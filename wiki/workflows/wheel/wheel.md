---
title: 轮动（Wheel）
created: 2026-06-16
updated: 2026-06-16
type: workflow
tags: [primary-course, intermediate-course, advanced-course, workflow, wheel, covered-call, cash-secured-put, yield]
sources: [D:\obsidian-vault\知识库\1.初级期权课程\第6章_期权的作用和案例展示\0603_第十五讲：期权的基本作用三 -- 收权利金.md]
confidence: high
contested: false
contradictions: []
---

# 轮动（Wheel）

Wheel 是把 Covered Call 和 Cash Secured Put 组合起来的长期循环策略。其本质不是“新策略”，而是两类正股 backed 卖方策略的系统化叠加。

## 标准流程

1. 卖 Put 接股：在目标标的、目标行权价卖出 Put，收取权利金。
2. 成功接股：被指派后持有正股，结余权利金已降低净买入成本。
3. 卖 Call：持有正股后卖出 OTM Call，继续收租金。
4. 若被 Call 走：正股以 Call 行权价卖出，锁定收益；重新回到第 1 步。
5. 若未被 Call 走：继续收租金，到期后换月重新卖 Call。

## 标准化要求

- 同一标的上，卖出的 CC 与 CSP 的张数必须匹配正股持仓，且比例维持 正股 股数 = Call/ Put 张数。
- 禁止裸卖：不能在没有正股或现金的情况下卖权。
- 双现金流：股息 + 权利金，两者共同构成长期复利。

## 市场环境适配

- 震荡市/温和上涨：Wheel 最稳定，现金流持续且波动率适中。
- 财报/宏观事件前：暂停 Wheel 新开仓，等 IV 高位卖权窗口。
- 强烈趋势行情（单边暴涨）：正股容易被 Call 走，需调整行权价或暂停卖 Call。

## 与定价和波动率的关系

- 在 IV 高位时卖 Put，能收到更高权利金，降低接股成本。
- 在 IV 高位时卖 Call，能获得高权利金，降低正股持仓成本。
- [[concepts/pricing|期权定价]]的偏离可辅助判断何时是 Wheel 节奏的高性价比窗口。

## 风险管理

- 单标的集中度：Wheel 是单标的多腿组合，容易出现“一单踩坑、整年白干”。
- 回撤纪律：若正股连续触发止损，需暂停标准 Wheel，转为观察期等待基本面向好。
- 再平衡：每季度回顾一次标的分布，防止整体仓位过于集中。

> **出处**：内容整合自初级课程收权利金及 Wheel 策略章节（^[课程:D:\obsidian-vault\知识库\1.初级期权课程\第 6 章_期权的作用和案例展示\0603_第十五讲：期权的基本作用三 -- 收权利金.md]）。
