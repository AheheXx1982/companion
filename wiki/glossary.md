---
title: Glossary
created: 2026-06-16
updated: 2026-06-16
type: glossary
tags: [meta, glossary, reference]
sources: []
confidence: high
contested: false
contradictions: []
---

# Glossary

<!-- Group entries by topic. Each term links back to the wiki page that explains it best. -->

## Strategy and Income Terms

- Covered Call — 持有正股的同时卖出虚值 Call，以换取权利金收入，同时接受收益封顶。
- Cash Secured Put (CSP) — 在账户中预留足额现金后卖出 Put，以获得接股机会和权利金。
- PMCC (Poor Man's Covered Call) — 用深度 ITM LEAP Call 替代正股做 Covered Call，降低建仓资本占用。
- Wheel Strategy — 通过 CSP 接股后转 CC、再卖 CSP 的循环机制，长期滚动产生现金流。
- Wheel 标准化 — 同一标的的 CC 与 CSP 必须保持 1:1 股/张匹配，避免裸卖空敞口。
- SBS (Sell Buy Spread) — 通过 Sell Put + Buy Put 的组合实现最大卖方优势的方法。
- Collar — 持有正股的同时买入 Put 保护、卖出 Call 补贴权利金，形成低成本对冲组合。
- Spread — 用两条不同行权价或到期日的期权构建方向性或波动率仓位，限制风险敞口。
- Straddle — 同时买入或卖出相同行权价、相同到期日的 Call 和 Put。
- Strangle — 同时买入或卖出不同行权价但相同到期日的 Call 和 Put。

## Instrument and Market Structure Terms

- ITM — In The Money：期权内在价值 > 0，持有者有行权价值。
- ATM — At The Money：期权内在价值 ≈ 0，对利率和 Gamma 最敏感。
- OTM — Out of The Money：期权内在价值 = 0，只有时间价值和波动率价值。
- BSM 模型 — Black-Scholes-Merton 期权定价模型，用于解释价格构成。
- IV (Implied Volatility) — 隐含波动率，期权价格由市场交易隐含出来的未来波动预期。
- Vega — 波动率敏感度：IV 变化 1 点时，期权价格变化的幅度。
- Theta — 时间价值衰减速度：期权价格每天因时间流逝而减少的金额。
- Delta — 方向敏感度：正股价格变化 1 美元时，期权价格的理论变化量。
- Gamma — Delta 的变化率：衡量 Delta 对正股价格变动的二次敏感度。

## Account and Assignment Terms

- Assignment — 期权卖方被分配行权义务：卖 Put 导致买入正股，卖 Call 导致卖出正股。
- Exercise — 期权买方主动行权，要求按约定价买入或卖出正股。
- Margin — 保证金账户中允许卖空期权或杠杆交易的额度体系。
- Liquidity — 流动性：期权市场买卖深度，决定能否以合理价快速成交。
- Rollover — 将现有到期仓位通过对冲后移至新合约，延长策略周期。

## Meta / Workflow Terms

- Sleep Test — 你是否能安心持有该策略过夜而不焦虑的直觉检验。
- Safety Margin — 安全边际：策略在劣化情景下仍能存活或保本的空间。
- Rebalance — 再平衡：按固定规则调整仓位以恢复目标风险水平。
- Sigma — sigma 安全边际：与标准差或波动率阈值挂钩的止损/风控边界。
