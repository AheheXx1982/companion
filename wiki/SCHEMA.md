---
title: Wiki Schema
created: 2026-06-16
updated: 2026-06-16
type: schema
tags: [meta, schema, options, wiki]
sources: []
confidence: high
contested: false
contradictions: []
---

# Wiki Schema

## Domain

美股期权课程知识体系：初级期权课程 + 中级期权课程 + 高级期权课程。
服务对象：投资者 SilentXx，目标是通过期权实现 **稳定现金流** 和 **长期复利**。
底层哲学：低波动、高胜率、可持续叠加、有 sigma 安全边际。

## Location Mapping

- Vault: `D:\obsidian-vault`
- Wiki root: `D:\obsidian-vault\wiki`
- 课程原始笔记: `D:\obsidian-vault\知识库\`
- SilentXx 期权实战: `D:\obsidian-vault\SilentXx期权实战\`

## Directory Layout

```plain
wiki/
├── SCHEMA.md
├── index.md
├── log.md
├── glossary.md
├── concepts/
│   ├── greeks/
│   ├── pricing/
│   ├── exercise-and-assignment/
│   ├── volatility/
│   └── yield-and-income/
├── entities/
│   ├── strategies/
│   └── tickers/
├── comparisons/
│   └── strategy-vs-strategy/
├── workflows/
│   ├── wheel/
│   ├── pmcc/
│   └── csp-selection/
└── queries/
```

## Front Matter (wiki pages only)

```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: concept | entity | comparison | workflow | query | glossary
tags: [from taxonomy]
sources: [source paths]
confidence: high | medium | low
contested: true | false
contradictions: []
---
```

Required keys: `title`, `created`, `updated`, `type`, `tags`, `sources`, `confidence`, `contested`.

## Tag Taxonomy

- Mechanisms: greeks, pricing, exercise, assignment, margin, liquidity, iv, vega, theta, delta, gamma
- Strategies: covered-call, cash-secured-put, wheel, pmcc, collar, spread, straddle, strangle, sbs
- Roles: buyer, seller, retail-trader, institutional-trader
- Markets: us-equities, cash-secured-account, margin-account
- Meta: comparison, workflow, risk, income, homework, open-question
- Course: primary-course, intermediate-course, advanced-course

## Page Rules

1. One page per concept or entity.
2. Each wiki page must have at least **2 outbound `[[wikilinks]]`** to other wiki pages.
3. Course notes remain the source of truth; wiki pages synthesize and cross-link them.
4. Keep pages scannable; split if exceeding 220 lines.
5. Write in Simplified Chinese; keep English abbreviations or terminology in parentheses where helpful.
6. Glossary entries use `- Term — definition` format, grouped by topic.
7. Provenance: when a claim traces back to a specific advanced lecture, mark it with `^[课程:<路径>]`.

## Source of Truth

- Course notes beats wiki when in conflict, unless the course note is marked as superseded or draft.
- Wiki should maintain backlinks to the underlying course notes.

## Index and Log

- Every wiki page must appear in `index.md` under the correct section.
- Every wiki action must appear in `log.md`.

## Lint Rules

- Flag orphan pages (no inbound links) after every migration.
- Flag broken `[[wikilinks]]` after every rename.
- Flag pages with `confidence: low` for review.
- Do not silently overwrite contradictions; use `contradictions:` in front matter.

## Migration Boundary

- Source material under `知识库/` is treated as **L1**. Never write `知识库/` during wiki operations.
- All generated wiki content must be written under `wiki/`.
