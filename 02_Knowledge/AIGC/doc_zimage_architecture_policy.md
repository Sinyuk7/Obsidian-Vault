---
title: 'doc_zimage_architecture_policy'
aliases:
  - 'Z-Image 架构与参数策略'
  - 'S3-DiT 推理策略'
tags:
  - AIGC
  - AIGC/Z-Image
  - AIGC/Model-Notes
  - AIGC/Prompt-Engineering
  - model-notes
  - imported/drive-download
  - source/docx
  - status/distilled
source_file: 'C:\Users\80998\Desktop\drive-download-20260523T041143Z-3-001\doc_zimage_architecture_policy.docx'
imported: 2026-05-23
original_format: docx
target_folder: '02_Knowledge/AIGC'
status: distilled
safety_review_required: false
---

# doc_zimage_architecture_policy
Last_Updated: 2026-05-23

## Overview
- Purpose: 蒸馏 z-image 或 S3-DiT 相关提示词架构、参数策略和安全边界，形成可复用的模型使用规范。
- Scope: Covers 推理管线参数、正向提示词结构、人物安全描述、文本生成、伪影诊断和清理约束。Does not cover 平台绕过、未经验证的内部架构、侵权或不安全内容生成。

## Core Concepts
- **S3-DiT 推理管线**: 以正向提示词为主要控制入口，负向提示词和 CFG 类引导不应默认启用。
- **Guidance Scale 0.0**: 当模型架构要求无 CFG 时，guidance_scale 应固定为 0.0，否则可能破坏模型预期行为。
- **Steps 8-12**: 原材料给出的推荐步数范围，用于在速度和画面稳定性之间平衡。
- **正向脚手架**: 镜头与主体、年龄与外观、服装与覆盖、环境、光影、情绪、风格媒介、技术说明、安全清理约束构成主结构。
- **安全与清理约束**: 用于减少肢体伪影、背景杂乱、多余人物、镜头畸变和不合规表达。
- **文本渲染约束**: 需要区分主要文本、次要文本、字体风格、排版关系和文本排他性。

## Consolidated Principles
- P1 [Critical]: guidance_scale 固定为 0.0，负面提示词输入保持为空，除非模型文档明确要求改变。
- P2 [Critical]: 人物提示必须显式锁定成人身份、服装覆盖和非性化上下文，避免年龄或场景歧义。
- P3 [High]: 正向提示词越结构化，模型越容易保持主体、空间和风格一致。
- P4 [High]: 修复伪影时优先追加正向清理约束，而不是使用否定词堆叠。
- P5 [High]: 固定 Seed 适合迭代同一提示词；随机 Seed 适合探索多样性。
- P6 [Normal]: 文本生成任务必须把文字内容、语言、层级和位置写清楚，不能只写 poster with text。

## Mechanisms & Logic
- Flow: 1. 初始化推理管线 -> 2. 设 guidance_scale 为 0.0 -> 3. 清空负面提示词 -> 4. 设 Steps 为 8-12 -> 5. 固定或随机 Seed -> 6. 输入结构化正向提示词。
- Prompt Structure: 镜头与主体；年龄与外观；服装与覆盖；环境背景；光影；情绪；风格媒介；技术说明；安全与清理约束。
- Diagnostic Rules: 肢体错误 -> 增加手部数量、关节方向、自然姿态和解剖一致性描述。
- Diagnostic Rules: 背景杂乱 -> 增加单主体、清晰背景、空间分层和无多余人物的正向描述。
- Diagnostic Rules: 文本错误 -> 限制文本数量，明确语言、大小写、位置和不出现额外文字。

## Constraints
- 不要填写负面提示词作为默认清理策略。
- 不要把 CFG、负向 prompt、长参数串当作通用增强器。
- 不要让年龄、服装、姿态或场景产生未成年人性化歧义。
- 不要在同一提示词里同时要求多个互斥主体、多个主视角或多个排版焦点。
- 不要把诊断项写成绕过审核或弱化安全边界的技巧。

## Output Format / Style Hints
- z-image Prompt Skeleton: camera and subject；adult identity and appearance；clothing and coverage；environment；lighting；mood；style or medium；technical notes；safety and cleanup constraints。
- Parameter Defaults: guidance_scale 0.0；negative prompt empty；steps 8-12；seed fixed for iteration or random for exploration。

## Related
- [[z-image_prompt_knowledge]]
- [[prohibited_guidelines]]
- [[Image understanding]]
- [[AI绘画审核规避实战指南|AI绘画合规风险与提示词边界指南]]
