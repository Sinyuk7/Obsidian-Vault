---
title: 'Midjourney Prompt Construction Standards'
aliases:
  - 'Midjourney 提示词构造标准'
tags:
  - AIGC
  - AIGC/Midjourney
  - AIGC/Prompt-Engineering
  - prompt-engineering
  - visual-design
  - imported/drive-download
  - source/docx
  - status/distilled
source_file: 'C:\Users\80998\Desktop\drive-download-20260523T041143Z-3-001\Midjourney Prompt Construction Standards.docx'
imported: 2026-05-23
original_format: docx
target_folder: '02_Knowledge/AIGC'
status: distilled
safety_review_required: false
---

# Midjourney Prompt Construction Standards
Last_Updated: 2026-05-23

## Overview
- Purpose: 建立 Midjourney 提示词构造标准，使自然语言、图像提示、参数和工作流形成可控结构。
- Scope: Covers V6/V6.1 语义理解、图像提示、文本提示、参数位置、风格化控制、多提示、个性化和运行限制。Does not cover 最新版本实时变更、违规内容规避、未经验证的模型内部实现。

## Core Concepts
- **自然语言范式**: V6 以后更偏向理解完整描述，关键词堆叠和 junk words 的收益下降。
- **图像提示**: 作为视觉锚点提供构图、角色、材质或风格参考，但需要文字说明保留和改变的部分。
- **叙事层级**: 主体、动作、环境、镜头、光影、风格和技术参数应按重要性排序。
- **参数语法**: aspect ratio、stylize、chaos、weird、quality、seed 等参数应放在提示词末尾并与模型版本匹配。
- **多提示与权重**: 用于分离概念和调节关注度，但会增加不可预测性。
- **个性化**: personalization 会引入用户偏好，适合风格稳定，不适合严格客观复现。

## Consolidated Principles
- P1 [Critical]: 提示词应写可见结果，不写创作意图或用途说明。
- P2 [Critical]: 参数不能替代主体、构图和光影描述；参数只调制已有语义。
- P3 [High]: 先写核心主体和动作，再写场景、镜头、光影、风格，最后写参数。
- P4 [High]: 版本能力差异必须显式标注，不能把 V6.1 的文本、手部或 upscaler 表现假定为所有版本通用。
- P5 [High]: 文本生成需要引号包裹目标文字，并限制额外文字。
- P6 [Normal]: 长 prompt 应删减重复形容词，为关键视觉细节保留注意力预算。

## Mechanisms & Logic
- Flow: 1. 选择模型版本 -> 2. 放置图像参考 -> 3. 写主体和动作 -> 4. 写镜头与构图 -> 5. 写材质光影风格 -> 6. 添加参数 -> 7. 迭代 seed 或 variation。
- Decision Rules: 需要稳定构图时降低 chaos，固定 seed，并减少互斥描述。
- Decision Rules: 需要风格探索时提高 stylize 或 chaos，但保留主体锚点。
- Decision Rules: 需要多对象时明确数量、位置和关系。
- Decision Rules: 需要文字时减少画面复杂度，让文字成为主要视觉任务。

## Constraints
- 不要使用 8K、HDR、award-winning 等弱控制词作为主要质量来源。
- 不要在同一 prompt 中混合多个镜头景别和多个主风格。
- 不要用否定句堆叠控制缺失对象，优先改写为正向状态。
- 不要把受版权保护角色名称当作复刻目标；应转成原创视觉特征和合法风格参考。
- 不要忽略平台政策和内容安全边界。

## Output Format / Style Hints
- Canonical Prompt: image references；main subject；action and pose；environment；camera and composition；lighting；materials and style；constraints；parameters。
- Parameter Placement: 所有 Midjourney 参数放末尾，避免混入自然语言主体描述。

## Related
- [[Midjourney 提示词规范与实践]]
- [[Midjourney 16_9 构图生成指南]]
- [[Midjourney 构图技巧与全身照]]
- [[midjourney_v7_best_practices]]
- [[midjourney-prompt-guide]]
- [[midjourney-prompt-best-practices]]
