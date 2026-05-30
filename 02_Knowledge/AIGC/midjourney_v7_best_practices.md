---
title: 'midjourney_v7_best_practices'
aliases:
  - 'Midjourney V7 Best Practices'
  - 'Midjourney V7 最佳实践'
tags:
  - AIGC
  - AIGC/Midjourney
  - AIGC/Prompt-Engineering
  - prompt-engineering
  - visual-design
  - imported/drive-download
  - source/docx
  - status/distilled
source_file: 'C:\Users\80998\Desktop\drive-download-20260523T041143Z-3-001\midjourney_v7_best_practices.docx'
imported: 2026-05-23
original_format: docx
target_folder: '02_Knowledge/AIGC'
status: distilled
safety_review_required: false
---

# midjourney_v7_best_practices
Last_Updated: 2026-05-23

## Overview
- Purpose: 汇总 Midjourney V7 使用中的高优先级约束，避免提示词过载、否定误导和主体失控。
- Scope: Covers 主体数量、否定句、祈使句、用途说明、自然语言描述、构图锚定和参数调制。Does not cover 实时官方更新、违规绕过、具体作品复刻。

## Core Concepts
- **主体数量限制**: 原材料将 Subject Count Limit 设为 4，超过后主体关系和细节稳定性显著下降。
- **无否定句**: V7 更适合接收正向可见描述，否定词可能激活不想要的概念。
- **无祈使句**: 模型不执行命令，它生成被描述的画面。
- **无用途说明**: for a poster、for marketing 等用途不会稳定转化为视觉结构。
- **自然语言短句**: 清晰、完整、可见的短句比关键词堆叠更稳定。
- **语义锚定**: 数量、位置、动作、材质和光影要明确到画面可见层。

## Consolidated Principles
- P1 [Critical]: 主体数量默认不超过 4；需要多主体时必须写位置、关系和层级。
- P2 [Critical]: 禁用 no、not、without、never 等否定表达，改写为目标状态。
- P3 [High]: 禁用祈使句和请求式语言，例如 make、create、show me。
- P4 [High]: 禁用用途说明，改写为可见版式、构图、文字或材质。
- P5 [High]: 每个关键视觉对象应有名词、属性和空间关系。
- P6 [Normal]: 参数应作为末端调制，不参与主体语法。

## Mechanisms & Logic
- Flow: 1. 删除命令和用途 -> 2. 把否定句改成正向状态 -> 3. 限制主体数量 -> 4. 明确位置和动作 -> 5. 添加风格与参数。
- Rewrite Rules: no logo -> plain unmarked surface。
- Rewrite Rules: without hat -> bare head with visible hair。
- Rewrite Rules: make it cinematic -> low-key lighting, wide composition, shallow depth of field, film still look。
- Decision Rules: 多主体场景优先指定主次，例如 one main subject with three background figures。

## Constraints
- 不要写超过模型可稳定处理的主体数量。
- 不要把列表式禁用项放进 prompt。
- 不要把意图、用途、评价和工作指令写给模型。
- 不要让同一名词被多个冲突形容词修饰。

## Output Format / Style Hints
- V7 Prompt Skeleton: visible subject；count and relationship；action；setting；composition；lighting；material and style；parameters。

## Related
- [[Midjourney Prompt Construction Standards]]
- [[Midjourney 提示词规范与实践]]
- [[Midjourney 16_9 构图生成指南]]
- [[Midjourney 构图技巧与全身照]]
- [[midjourney-prompt-best-practices]]
