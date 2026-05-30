---
title: 'Midjourney 提示词规范与实践'
aliases:
  - 'Midjourney Prompt Practice'
tags:
  - AIGC
  - AIGC/Midjourney
  - AIGC/Prompt-Engineering
  - prompt-engineering
  - visual-design
  - imported/drive-download
  - source/docx
  - status/distilled
source_file: 'C:\Users\80998\Desktop\drive-download-20260523T041143Z-3-001\Midjourney 提示词规范与实践.docx'
imported: 2026-05-23
original_format: docx
target_folder: '02_Knowledge/AIGC'
status: distilled
safety_review_required: false
---

# Midjourney 提示词规范与实践
Last_Updated: 2026-05-23

## Overview
- Purpose: 将 Midjourney V7 语境下的提示词实践压缩为可执行规范，强调自然语言、明确视觉目标和迭代控制。
- Scope: Covers V7 范式、标准 prompt 框架、语义精确性、参数调制、风格控制和常见失败修正。Does not cover 实时官方版本差异、平台绕过、侵权复刻。

## Core Concepts
- **V7 范式转移**: 提示词从关键词堆砌转向自然语言视觉描述，模型更依赖语境和关系。
- **标准提示词框架**: 主体、环境、动作、构图、光影、材质、风格、技术参数构成基本顺序。
- **语义精确性**: 模型执行的是可见描述，不是抽象赞美词或创作者意图。
- **歧义消除**: 数量、位置、关系、尺度和动作必须明确，否则模型会用训练数据原型补全。
- **迭代控制**: 固定 seed、局部变化、参数微调和 prompt 删减构成稳定工作流。
- **注意力预算**: prompt 越长，关键要素被稀释的概率越高。

## Consolidated Principles
- P1 [Critical]: 每个提示词必须有一个明确主目标，避免多个主体或风格同时争夺焦点。
- P2 [Critical]: 不要把用途说明、审美评价或祈使句当成视觉描述。
- P3 [High]: 先锁定主体和构图，再追加风格；风格不能补救结构不清。
- P4 [High]: 关键约束要前置，次要材质和背景后置。
- P5 [High]: 失败修正优先删减冲突词，再增加精确锚点。
- P6 [Normal]: 参数调制用于探索范围，不能替代 prompt 的语义清晰度。

## Mechanisms & Logic
- Flow: 1. 写一句可见目标 -> 2. 拆分主体、环境、构图、光影、风格 -> 3. 去掉抽象词 -> 4. 添加模型参数 -> 5. 固定 seed 迭代 -> 6. 根据失败类型修正。
- Failure Mapping: 裁切错误 -> 增加景别与边距；主体错乱 -> 减少数量并明确位置；风格跑偏 -> 前置风格媒介并删除冲突风格；细节丢失 -> 缩短 prompt。
- Decision Rules: 若需要强风格一致，使用风格参考或 personalization；若需要准确执行，降低风格化强度。

## Constraints
- 不要堆叠 beautiful、masterpiece、ultra detailed 等弱信号词。
- 不要让 prompt 同时要求写实照片、二次元插画、油画和 3D 渲染。
- 不要用 or、maybe、various 等选择逻辑。
- 不要用 no、not、without 作为主要控制方式。

## Output Format / Style Hints
- Prompt Skeleton: 一个清晰主体；一个动作或状态；一个空间环境；一个镜头构图；一组光影色彩；一种风格媒介；必要参数。

## Related
- [[Midjourney Prompt Construction Standards]]
- [[Midjourney 16_9 构图生成指南]]
- [[Midjourney 构图技巧与全身照]]
- [[midjourney_v7_best_practices]]
- [[midjourney-prompt-guide]]
- [[midjourney-prompt-best-practices]]
